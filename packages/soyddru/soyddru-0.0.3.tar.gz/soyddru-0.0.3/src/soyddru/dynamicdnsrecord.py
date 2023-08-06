import requests
import configparser
import os


class DynamicDnsRecordUpdator:
    """A class used to update a DNS record."""

    def __init__(self, get_public_ip_hostname=None, public_ip_storage_file=None,
                 update_dns_record_request_template=None, domain_name=None, dns_service_username=None,
                 dns_service_password=None):
        """
        :param str get_public_ip_hostname: the host url of the API used for fetching this machine's public IP
        :param str public_ip_storage_file: the name of the file used to store this machine's last known public IP
        :param str update_dns_record_request_template: the request url template for the API call to update the DNS
                record - contains variable placeholders for the domain name and public ip, respectively
        :param str domain_name: the domain name to update on the DNS record
        :param str dns_service_username: the username used for authenticating against the DNS record API
        :param str dns_service_password: the password used for authenticating against the DNS record API
        """
        config = configparser.ConfigParser(os.environ)
        config.read('../../config.ini')

        self.get_public_ip_hostname = get_public_ip_hostname or config.get('public.ip.getter', 'host')
        self.public_ip_storage_file = public_ip_storage_file or config.get('public.ip.history', 'file')
        self.domain_name = domain_name or config.get('dns.record.updater', 'request_template')
        self.update_dns_record_request_template = update_dns_record_request_template or \
                                                  config.get('dns.record.updater', 'domain')
        self.dns_service_username = dns_service_username or config.get('dns.record.updater', 'username')
        self.dns_service_password = dns_service_password or config.get('dns.record.updater', 'password')

    def update(self):
        """
        Updates the DNS record based on the class configuration. The DNS record is only updated if the public IP of the
        executing machine has changed.

        :return: str message indicating whether the DNS record has been updated or not.
        """
        current_public_ip = self.__get_public_ip(self.get_public_ip_hostname)

        if self.__handle_changed_ip(current_public_ip):
            response = self.__update_dns_record(current_public_ip)
            print("The public IP changed. DNS record update status is: " + str(response))

    @staticmethod
    def __get_public_ip(hostname):
        return requests.get(hostname).content.decode('utf8')

    def __handle_changed_ip(self, ip):
        with open(self.public_ip_storage_file, "a+") as public_ip_file:
            public_ip_file.seek(0)
            prev_public_ip = public_ip_file.read()
            if ip != prev_public_ip:
                public_ip_file.truncate(0)
                public_ip_file.write(ip)
                return True
            else:
                return False

    def __update_dns_record(self, ip):
        request_url = str.format(self.update_dns_record_request_template, self.domain_name, ip)
        print(f"Sending request to {request_url} ...")
        return requests.post(request_url, auth=(self.dns_service_username, self.dns_service_password))


import time
import os
import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from src import dynamicdnsrecord

config = configparser.ConfigParser()
config.read('../config.ini')

polling_interval_secs = int(config.get('polling.interval', 'seconds'))


def job(dns_record_updater_param):
    dns_record_updater_param.update()


def start():
    dns_record_updater = dynamicdnsrecord.DynamicDnsRecordUpdator()

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone='utc')

    scheduler.add_job(job, 'interval', args=[dns_record_updater], seconds=polling_interval_secs)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


if __name__ == '__main__':
    start()

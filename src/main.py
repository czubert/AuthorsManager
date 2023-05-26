from datetime import datetime

import src.aggregate as aggregate
import src.utils as utils

# import aggregate as aggregate
# import utils as utils


class AuthorList:
    def __init__(self):
        self.main_file = None
        self.not_sent = None
        self.file_names = None
        self.main_ready = False
        self.update_ready = False
        self.pynsist_prefix = 'pkgs/src'

    def data_update(self):
        lists_as_df = aggregate.read_lists_as_df(self.file_names)
        self.main_file = aggregate.concat_all_authors(self.main_file, lists_as_df)  # concatenating all gathered authors

        if self.main_file.empty:
            raise Exception('Update failed. Copy paste data file to "to_update" folder and try again.')

        return aggregate.aggregate_data(self.main_file)

    def create_db_of_n_authors(self, n_auth):
        # Choosing authors to send to and marks as sent
        # (sendinblue - up to 300 mails/day)
        # taking only emails that were not yet used
        mask = self.main_file['sent'] == 0  # takes only not sent authors
        self.not_sent = self.main_file[mask].iloc[:n_auth, :]
        self.not_sent['sent'] = 1

        # Store
        time = datetime.now()
        date_time = f'{time.year}-{time.month}-{time.day}_{time.hour}-{time.minute}-{time.second}'
        file_name = f'{self.pynsist_prefix}/to_send/{date_time}_{n_auth}_to_send'
        self.not_sent.to_excel(f'{file_name}.xlsx', index=False, encoding='utf-8')
        self.main_file.update(self.not_sent, errors='ignore')

    def check_if_main_ready(self):
        # Checking if ready to get authors for emails sending
        # Reading parsed data
        self.main_file = utils.read_csv_as_df(f'{self.pynsist_prefix}/database/main_file.csv')
        if not self.main_file.empty:
            self.main_ready = True

    def check_if_ready_for_update(self):
        # Checks if ready for update - if there are new files
        self.file_names = utils.get_file_names()
        if self.file_names:
            self.update_ready = True

    def store_main_db(self):
        self.main_file.to_csv(f'{self.pynsist_prefix}/database/main_file.csv', index=False, encoding='utf-16')

    def main(self):
        self.check_if_main_ready()
        self.check_if_ready_for_update()

        if not self.update_ready and not self.main_ready:
            raise Exception('Main file is empty, and there are no files to update it.')

        if self.update_ready:
            self.main_file = self.data_update()

        if self.main_ready:
            self.create_db_of_n_authors(n_auth=300)

        # Store
        self.store_main_db()


if __name__ == '__main__':
    authors = AuthorList()
    authors.main()

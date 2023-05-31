import pandas as pd
import re

from colorama import Fore, Style
import argparse


class LogDocker():
    columns = ["date", "host", "process", "pid", "log_time", "level", "message", "file", "component", "subcomponent"]

    def __init__(self, filename):
        self.df = pd.DataFrame(columns=self.columns)
        self.filename = filename

        with open(self.filename, 'r') as file:
            self.log_lines = file.readlines()

        self.process_logs()

    def process_logs(self):
        regex = re.compile(
            r"(?P<date>\w+\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\w+)\s+(?P<process>\w+)\[(?P<pid>\d+)\]:\s+time=\"(?P<log_time>[^\"]+)\"\s+level=(?P<level>\w+)\s+msg=\"(?P<message>[^\"]+)\"\s+file=\"(?P<file>[^\"]+)\"\s+component=(?P<component>[^\"]+)(\s+pkg=(?P<subcomponent>[^\"]+))?")

        for line in self.log_lines:
            match = regex.match(line)
            if match:
                groups = match.groupdict()
                self.process_component_subcomponent(groups)
                self.df = pd.concat([self.df, pd.DataFrame([groups])], ignore_index=True)

    def process_component_subcomponent(self, groups):
        if groups['component']:
            # Split into component and subcomponent if possible
            comp_split = groups['component'].split(' pkg=')
            groups['component'] = comp_split[0].replace('\n', '').replace('"', '').strip()
            if len(comp_split) > 1:
                groups['subcomponent'] = 'pkg=' + comp_split[1].replace('\n', '').replace('"', '').strip()

        # Just clean up the subcomponent field if it exists and wasn't just set
        if groups['subcomponent']:
            groups['subcomponent'] = groups['subcomponent'].replace('\n', '').replace('"', '').strip()

    def write_to_csv(self, output_filename):
        self.df.to_csv(output_filename, index=False)

    def get_logs_by_level(self, level):
        filtered_df = self.df[self.df['level'] == level]
        return filtered_df

    def get_logs_by_component(self, component):
        # Filter logs based on whether the 'component' field contains the desired string
        filtered_df = self.df[self.df['component'].str.contains(component, na=False)]
        return filtered_df

    def get_logs_by_subcomponent(self, subcomponent):
        # Filter logs based on whether the 'subcomponent' field contains the desired string
        filtered_df = self.df[self.df['subcomponent'].str.contains(subcomponent, na=False)]
        return filtered_df

    def get_logs_by_file(self, file):
        filtered_df = self.df[self.df['file'].str.contains(file, na=False)]
        return filtered_df

    def get_info_logs(self):
        return self.colorize_dataframe(self.get_logs_by_level('info'))

    def get_error_logs(self):
        return self.colorize_dataframe(self.get_logs_by_level('error'))

    def get_warning_logs(self):
        return self.colorize_dataframe(self.get_logs_by_level('warning'))

    def get_aws_logs(self):
        return self.colorize_dataframe(self.get_logs_by_component('porx/pkg/objectstore'))

    def get_storage_logs(self):
        return self.colorize_dataframe(self.get_logs_by_component('porx/storage/driver/volume'))

    def get_cloudsnap_backup_logs(self):
        return self.colorize_dataframe(self.get_logs_by_file('cloudsnap_backup.go'))

    def colorize_dataframe(self, df):
        output = []
        headers = df.columns.tolist()
        output.append(Fore.GREEN + " | ".join(headers) + Style.RESET_ALL)  # headers in green color
        for idx, row in df.iterrows():
            color = None
            if row['level'] == 'info':
                color = Fore.GREEN
            elif row['level'] == 'warning':
                color = Fore.YELLOW
            elif row['level'] == 'error':
                color = Fore.RED
            else:
                color = Style.RESET_ALL
            row_str = " | ".join(str(i) for i in row)
            output.append(color + row_str + Style.RESET_ALL)
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Process some logs.')
    parser.add_argument('--file', help='The log file to process')
    parser.add_argument('--info', action='store_true', help='Display info logs')
    parser.add_argument('--error', action='store_true', help='Display error logs')
    parser.add_argument('--warning', action='store_true', help='Display warning logs')
    parser.add_argument('--aws', action='store_true', help='Display AWS logs')
    parser.add_argument('--storage', action='store_true', help='Display storage logs')
    parser.add_argument('--cloudsnap', action='store_true', help='Display cloudsnap backup logs')
    args = parser.parse_args()

    log_docker = LogDocker(args.file)
    log_docker.write_to_csv('output.csv')

    if args.info:
        print(log_docker.get_info_logs())
    if args.error:
        print(log_docker.get_error_logs())
    if args.warning:
        print(log_docker.get_warning_logs())
    if args.aws:
        print(log_docker.get_aws_logs())
    if args.storage:
        print(log_docker.get_storage_logs())
    if args.cloudsnap:
        print(log_docker.get_cloudsnap_backup_logs())


if __name__ == "__main__":
    main()
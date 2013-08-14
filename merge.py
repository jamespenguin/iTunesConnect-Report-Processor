#!/usr/bin/env python
#
# iTunes Connect Earnings Report Merger Script
# By Brandon Smith (brandon.smith@studiobebop.net)
#
import os, csv, json
import requests

###
# Config
###

app_id         = "" # Your account's API access app ID.
                    # You get this by registering an account on openexchangerates.org
exchange_rates = requests.get("http://openexchangerates.org/api/latest.json?app_id=%s" % app_id).content
exchange_rates = json.loads(exchange_rates)["rates"]

#!# End Config #!#

if __name__ == '__main__':
    # read file data into an array
    raw_reports = []
    for path, dirs, files in os.walk("."):
        report_name = os.path.split(os.path.abspath("."))[-1]
        for file_name in files:
            if not file_name.endswith(".txt"):
                continue
            report = open(file_name, "r").read()
            raw_reports.append(report)

    # Iterate through each report, and parse out all report data that we want
    processed_reports = []
    products = {}
    for raw_report in raw_reports:
        print "[+] Processing report -- %d / %d" % (raw_reports.index(raw_report)+1, len(raw_reports))
        report_lines = []
        for line in raw_report.split("\n"):
            line = line.split("\t")
            if len(line) < 20 or line[0].startswith("Start "):
                continue
            # Parse out all the data we want
            report_line = {}
            report_line["quantity"] = line[5]
            report_line["currency"] = line[8].upper()
            report_line["title"] = line[12]

            # Calculate earnings in USD
            report_line["earnings"] = float(line[7])
            if report_line["earnings"] < 1:
                continue
            if report_line["currency"] != "USD":
                converted_currency = report_line["earnings"] / exchange_rates[report_line["currency"]]
                report_line["earnings"] = converted_currency
            report_lines.append(report_line)

            # Update the products dictionary
            if not products.has_key(report_line["title"]):
                products[report_line["title"]] = {"earnings": 0.0}
            products[report_line["title"]]["earnings"] += report_line["earnings"]

        processed_reports.append(report_lines)

    # Output a nice pretty new report file from our processed data
    output_file = open("%s Earnings Report.csv" % report_name, "w")
    writer = csv.writer(output_file)

    product_names = products.keys()
    product_names.sort()

    writer.writerow(["Product", "Earnings (USD)"])
    for product_name in product_names:
        product = products[product_name]
        writer.writerow([product_name, "$%0.2f" % product["earnings"]])
    total_earned = sum(map(lambda x: products[x]["earnings"], product_names))
    writer.writerow(["TOTAL", "$%0.2f" % total_earned])

    output_file.close()

    print "-" * 75
    print "[+] Done!"
    raw_input("[+] Press enter to exit.")






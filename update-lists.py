import csv


csv_filename = "domains.csv"

list_names = ["beta", "main","borked"]

lists = {
	"beta": [],
	"main": [],
	"borked": []
}


output_filenames = {
	"beta": "telemetry-domains_beta.txt",
	"main": "telemetry-domains.txt",
	"borked": "telemetry-domains_borked.txt"
}

autogen_notice = [
	["#"],
	["# This list was generated automatically"],
	["# Please refer to the UPDATING.md file for instructions on how to make changes to these blocklists"],
	["# Any edits directly to this file will be overwritten"],
	["#"]
]

def populate_lists():
	with open(csv_filename) as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			if row.get("list") in list_names:
				lists[row.get("list")].append(row)


def dedup_list(list_name):
	the_list = lists[list_name]
	deduplicated = []

	for row in the_list:
		domain = row.get("raw_domain")
		if domain is not None and domain not in deduplicated:
			deduplicated.append(domain)
	
	lists[list_name] = deduplicated

	

def output_list(list_name):
	the_list = lists[list_name]
	outfile = output_filenames[list_name]
	the_list = sorted(the_list)
	with open(outfile, 'w') as csvfile:
		writer = csv.writer(csvfile, dialect='unix', quoting=csv.QUOTE_NONE)
		for line in autogen_notice:
			writer.writerow(line)
		for domain in the_list:
			writer.writerow([domain])
	
	
	
		


populate_lists()

print("updating beta list")
dedup_list("beta")
output_list("beta")

print("updating main list")
dedup_list("main")
output_list("main")

print("updating borked list")
dedup_list("borked")
output_list("borked")

print("Done.")
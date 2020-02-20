import xml.etree.cElementTree as ET
import sys
from analysis import utility_comp
import subprocess
import os


def parse_args():
    args = list(sys.argv)
    agent = args[1]
    opponents = parse_opponents(args[2])
    domains = parse_domains(args[3])
    return agent, opponents, domains


def parse_domains(filename):
    with open(filename, 'r') as file:
        domains = file.read().splitlines()
        domains = [[domains[i], domains[i + 1]] for i in range(len(domains) // 2)]
    return domains


def parse_opponents(filename):
    with open(filename, 'r') as file:
        opponents = file.read().splitlines()
    return opponents


def make_xml(agent1, agent2, domain):
    root = ET.Element("multilateralTournamentsConfiguration")
    doc = ET.SubElement(root, "tournaments")
    doc2 = ET.SubElement(doc, "tournament")
    doc3 = ET.SubElement(doc2, "deadline")
    ET.SubElement(doc3, "value").text = "20"
    ET.SubElement(doc3, "type").text = "TIME"
    my_attributes = {"hasMediatorProfile": "false", "hasMediator": "false",
                     "description": "Each agents makes offer, counter-offer, or accepts",
                     "classPath": "genius.core.protocol.StackedAlternatingOffersProtocol",
                     "protocolName": "Stacked Alternating Offers Protocol for Multi-Lateral Negotiation (SAOPMN)"}
    ET.SubElement(doc2, "protocolItem", attrib=my_attributes)
    doc4 = ET.SubElement(doc2, "partyRepItems")

    my_attributes2 = {"classPath": agent1}
    doc5 = ET.SubElement(doc4, "party", attrib=my_attributes2)
    ET.SubElement(doc5, "properties")

    my_attributes3 = {"classPath": agent2}
    doc6 = ET.SubElement(doc4, "party", attrib=my_attributes3)
    ET.SubElement(doc6, "properties")

    doc7 = ET.SubElement(doc2, "partyProfileItems")
    ET.SubElement(doc7, "item", url=domain[0])
    ET.SubElement(doc7, "item", url=domain[1])

    ET.SubElement(doc2, "repeats").text = "1"
    ET.SubElement(doc2, "numberOfPartiesPerSession").text = "2"
    ET.SubElement(doc2, "repetitionAllowed").text = "false"
    ET.SubElement(doc2, "persistentDataType").text = "DISABLED"

    tree = ET.ElementTree(root)
    tree.write("tournaments/.tmp.xml")


def run_tournament():
    p = subprocess.Popen(["powershell.exe",
                          "sh/analysis.ps1"])
    p.communicate()


def merge_csv():
    with open('log/.tmp.csv', 'r') as file:
        original = file.read()

    with open('log/results.csv', 'a') as file:
        original = original.split('\n')
        for line in original[2:-1]:
            file.write(f'{line}\n')


def analysis(agent):
    name = agent.split('/')
    name = name[len(name)-1].split('.')
    name = name[len(name)-2]
    utility_comp(name)


def cleanup():
    os.remove("log/.tmp.csv")


def make_results_file():
    header = 'sep=;\n' \
             'Run time (s);Round;Exception;deadline;Agreement;Discounted;#agreeing;min.util.;max.util.;' \
             'Dist. to Pareto;Dist. to Nash;Social Welfare;Agent 1;Agent 2;Utility 1;Utility 2;' \
             'Disc. Util. 1;Disc. Util. 2;Perceived. Util. 1;Perceived. Util. 2;User Bother 1;' \
             'User Bother 2;User Util. 1;User Util. 2;Profile 1;Profile 2'

    with open('log/results.csv', 'w') as file:
        file.write(f'{header}\n')


def main():
    agent, opponents, domains = parse_args()

    make_results_file()

    for opponent in opponents:
        for domain in domains:
            make_xml(agent, opponent, domain)
            run_tournament()
            merge_csv()

    analysis(agent)
    cleanup()


if __name__ == '__main__':
    main()

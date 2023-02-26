import sys
import xml.etree.ElementTree as ET

def read_xml(file):
	tree = ET.parse(file)
	root = tree.getroot()
	sql = create_table(root)
	return sql

def get_type(node):
	data_type = node.attrib['type']
	if data_type == 'int':
		return 'int'

def create_column(node):
	name = node.attrib['name']
	data_type = node.attrib['type']
	sql = name + ' ' + get_type(node)
	return sql

def get_columns(node):
	columns = []
	for child in node:
		if child.tag == 'column':
			column = create_column(child)
			columns.append(column)
	return ','.join(columns)

def save_to_file(sql, file):
	f = open(file, 'w')
	f.write(sql)
	f.close()

def create_table(node):
	attributes = node.attrib
	name = attributes['name']
	comment = attributes['comment']
	columns = get_columns(node)
	if not comment:
		sql = 'CREATE TABLE ' + name + ' (' + columns + ');'
	else:
		sql = "CREATE TABLE " + name + " (" + columns + ") COMMENT='" + comment + "';"
	return sql

sql = read_xml(sys.argv[1])
save_to_file(sql, sys.argv[2])
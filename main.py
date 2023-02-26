import sys
import xml.etree.ElementTree as ET

def read_xml(file):
	tree = ET.parse(file)
	root = tree.getroot()
	sql = create_table(root)
	return sql

def get_nullable(node):
	try:
		nullable = node.attrib['nullable']
	except KeyError:
		return ''
	else:
		if nullable == 'false':
			return ' NOT NULL'
		elif nullable == 'true':
			return ''

def get_unsigned(node):
	try:
		unsigned = node.attrib['unsigned']
	except KeyError:
		return ''
	else:
		if unsigned == 'true':
			return ' UNSIGNED'
		elif unsigned == 'false':
			return ''

def get_comment(node):
	try:
		comment = node.attrib['comment']
	except KeyError:
		return ''
	else:
		return " COMMENT '" + comment + "'"

def get_length(node):
	length = node.attrib['length']
	return '(' + length + ')'

def get_default_numeric(node):
	try:
		default = node.attrib['default']
	except KeyError:
		return ''
	else:
		return ' DEFAULT ' + default

def get_default_string(node):
	try:
		default = node.attrib['default']
	except KeyError:
		return ''
	else:
		return " DEFAULT '" + default + "'"

def get_precision(node):
	precision = node.attrib['precision']
	scale = node.attrib['scale']
	return '(' + ','.join([precision, scale]) + ')'

def get_type(node):
	data_type = node.attrib['type']
	if data_type == 'int':
		return 'INT' + get_unsigned(node) + get_default_numeric(node)
	elif data_type == 'float':
		return 'FLOAT' + get_default_numeric(node)
	elif data_type == 'varchar':
		return 'VARCHAR' + get_length(node) + get_default_string(node)
	elif data_type == 'text':
		return 'TEXT'
	elif data_type == 'blob':
		return 'BLOB'

def create_column(node):
	name = node.attrib['name']
	data_type = node.attrib['type']
	sql = name + ' ' + get_type(node) + get_nullable(node) + get_comment(node)
	return sql

def get_columns(node):
	columns = []
	for child in node:
		if child.tag == 'column':
			column = create_column(child)
			columns.append(column)
	return ', '.join(columns)

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
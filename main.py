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

def get_default_datetime(node):
	try:
		default = node.attrib['default']
	except KeyError:
		return ''
	else:
		if default == 'CURRENT_TIMESTAMP':
			return " DEFAULT CURRENT_TIMESTAMP"
		return ''

def get_precision(node):
	try:
		precision = node.attrib['precision']
		scale = node.attrib['scale']
	except KeyError:
		return ''
	else:
		return '(' + ','.join([precision, scale]) + ')'

def get_auto_increment(node):
	try:
		identity = node.attrib['identity']
	except KeyError:
		return ''
	else:
		if identity == 'true':
			return ' AUTO_INCREMENT'
		return ''

def get_type(node):
	data_type = node.attrib['type']
	if data_type == 'int':
		return 'INT' + get_unsigned(node) + get_auto_increment(node) + get_default_numeric(node)
	elif data_type == 'float':
		return 'FLOAT' + get_default_numeric(node)
	elif data_type == 'real':
		return 'REAL' + get_default_numeric(node)
	elif data_type == 'decimal':
		return 'DECIMAL' + get_precision(node) + get_default_numeric(node)
	elif data_type == 'varchar':
		return 'VARCHAR' + get_length(node) + get_default_string(node)
	elif data_type == 'text':
		return 'TEXT'
	elif data_type == 'blob':
		return 'BLOB'
	elif data_type == 'date':
		return 'DATE'
	elif data_type == 'datetime':
		return 'DATETIME' + get_default_datetime(node)
	elif data_type == 'timestamp':
		return 'TIMESTAMP' + get_default_datetime(node)

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
	return ',\n'.join(columns)

def get_primary_key_columns(node):
	columns = []
	for child in node:
		if child.tag == 'column':
			name = child.attrib['name']
			columns.append(name)
	return ','.join(columns)

def get_unique_columns(node):
	columns = []
	for child in node:
		if child.tag == 'column':
			name = child.attrib['name']
			columns.append(name)
	return ','.join(columns)

def create_constraint(node):
	data_type = node.attrib['type']
	if data_type == 'primary':
		columns = get_primary_key_columns(node)
		return 'PRIMARY KEY (' + columns + ')'
	elif data_type == 'foreign':
		name = node.attrib['referenceId']
		column = node.attrib['column']
		reference_table = node.attrib['referenceTable']
		reference_column = node.attrib['referenceColumn']
		on_delete = node.attrib['onDelete']
		return 'CONSTRAINT ' + name + ' FOREIGN KEY (' + column + ') REFERENCES ' + reference_table + '(' + reference_column + ') ON DELETE ' + on_delete
	elif data_type == 'unique':
		columns = get_unique_columns(node)
		name = node.attrib['referenceId']
		return 'CONSTRAINT ' + name + ' UNIQUE (' + columns + ')'

def get_constraints(node):
	constraints = []
	for child in node:
		if child.tag == 'constraint':
			constraint = create_constraint(child)
			constraints.append(constraint)
	return ',\n'.join(constraints)

def save_to_file(sql, file):
	f = open(file, 'w')
	f.write(sql)
	f.close()

def get_index_columns(node):
	columns = []
	for child in node:
		if child.tag == 'column':
			column = child.attrib['name']
			columns.append(column)
	return ','.join(columns)

def create_index(node):
	name = node.attrib['referenceId']
	columns = get_index_columns(node)
	return 'INDEX (' + columns + ')'

def get_indexes(node):
	indexes = []
	for child in node:
		if child.tag == 'index':
			index = create_index(child)
			indexes.append(index)
	return ',\n'.join(indexes)

def create_table(node):
	attributes = node.attrib
	name = attributes['name']
	sql = 'CREATE TABLE ' + name + '(\n' + get_columns(node) + ',\n' + get_constraints(node) + ',\n' + get_indexes(node) + ')\n' + get_comment(node) + ';'
	return sql

sql = read_xml(sys.argv[1])
save_to_file(sql, sys.argv[2])
NUMBER_TYPE = {'type': 'number'}
STRING_TYPE = {'type': 'string'}
INTEGER_TYPE = {'type': 'integer'}
BOOLEAN_TYPE = {'type': 'boolean'}
NULL_TYPE = {'type': 'null'}
EMAIL_TYPE = {'type': 'string'}
DATE_TYPE = STRING_TYPE
FLOAT_TYPE = NUMBER_TYPE

# Nullable schema ###
NULLABLE_STRING_TYPE = {'anyOf': [STRING_TYPE, NULL_TYPE]}
NULLABLE_INTERGER_TYPE = {'anyOf': [INTEGER_TYPE, NULL_TYPE]}
NULLABLE_NUMBER_TYPE = {'anyOf': [NUMBER_TYPE, NULL_TYPE]}
NULLABLE_FLOAT_TYPE = NULLABLE_NUMBER_TYPE

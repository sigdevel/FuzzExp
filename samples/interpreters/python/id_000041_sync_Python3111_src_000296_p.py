


import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2


_sym_db = _symbol_database.Default()


import google.protobuf.unittest_import_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/protobuf/unittest.proto',
  package='protobuf_unittest',
  serialized_pb=_b('\n\x1egoogle/protobuf/unittest.proto\x12\x11protobuf_unittest\x1a%google/protobuf/unittest_import.proto\"\xed\x18\n\x0cTestAllTypes\x12\x16\n\x0eoptional_int32\x18\x01 \x01(\x05\x12\x16\n\x0eoptional_int64\x18\x02 \x01(\x03\x12\x17\n\x0foptional_uint32\x18\x03 \x01(\r\x12\x17\n\x0foptional_uint64\x18\x04 \x01(\x04\x12\x17\n\x0foptional_sint32\x18\x05 \x01(\x11\x12\x17\n\x0foptional_sint64\x18\x06 \x01(\x12\x12\x18\n\x10optional_fixed32\x18\x07 \x01(\x07\x12\x18\n\x10optional_fixed64\x18\x08 \x01(\x06\x12\x19\n\x11optional_sfixed32\x18\t \x01(\x0f\x12\x19\n\x11optional_sfixed64\x18\n \x01(\x10\x12\x16\n\x0eoptional_float\x18\x0b \x01(\x02\x12\x17\n\x0foptional_double\x18\x0c \x01(\x01\x12\x15\n\roptional_bool\x18\r \x01(\x08\x12\x17\n\x0foptional_string\x18\x0e \x01(\t\x12\x16\n\x0eoptional_bytes\x18\x0f \x01(\x0c\x12\x44\n\roptionalgroup\x18\x10 \x01(\n2-.protobuf_unittest.TestAllTypes.OptionalGroup\x12N\n\x17optional_nested_message\x18\x12 \x01(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessage\x12\x43\n\x18optional_foreign_message\x18\x13 \x01(\x0b\x32!.protobuf_unittest.ForeignMessage\x12H\n\x17optional_import_message\x18\x14 \x01(\x0b\x32\'.protobuf_unittest_import.ImportMessage\x12H\n\x14optional_nested_enum\x18\x15 \x01(\x0e\x32*.protobuf_unittest.TestAllTypes.NestedEnum\x12=\n\x15optional_foreign_enum\x18\x16 \x01(\x0e\x32\x1e.protobuf_unittest.ForeignEnum\x12\x42\n\x14optional_import_enum\x18\x17 \x01(\x0e\x32$.protobuf_unittest_import.ImportEnum\x12!\n\x15optional_string_piece\x18\x18 \x01(\tB\x02\x08\x02\x12\x19\n\roptional_cord\x18\x19 \x01(\tB\x02\x08\x01\x12U\n\x1eoptional_public_import_message\x18\x1a \x01(\x0b\x32-.protobuf_unittest_import.PublicImportMessage\x12P\n\x15optional_lazy_message\x18\x1b \x01(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessageB\x02(\x01\x12\x16\n\x0erepeated_int32\x18\x1f \x03(\x05\x12\x16\n\x0erepeated_int64\x18  \x03(\x03\x12\x17\n\x0frepeated_uint32\x18! \x03(\r\x12\x17\n\x0frepeated_uint64\x18\" \x03(\x04\x12\x17\n\x0frepeated_sint32\x18"9\n\nNestedEnum\x12\x07\n\x03\x46OO\x10\x01\x12\x07\n\x03\x42\x41R\x10\x02\x12\x07\n\x03\x42\x41Z\x10\x03\x12\x10\n\x03NEG\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x42\r\n\x0boneof_field\"|\n\x12NestedTestAllTypes\x12\x34\n\x05\x63hild\x18\x01 \x01(\x0b\x32%.protobuf_unittest.NestedTestAllTypes\x12\x30\n\x07payload\x18\x02 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\"4\n\x14TestDeprecatedFields\x12\x1c\n\x10\x64\x65precated_int32\x18\x01 \x01(\x05\x42\x02\x18\x01\"\x1b\n\x0e\x46oreignMessage\x12\t\n\x01\x63\x18\x01 \x01(\x05\"\x1d\n\x11TestAllExtensions*\x08\x08\x01\x10\x80\x80\x80\x80\x02\"$\n\x17OptionalGroup_extension\x12\t\n\x01\x61\x18\x11 \x01(\x05\"$\n\x17RepeatedGroup_extension\x12\t\n\x01\x61\x18/ \x01(\x05\"\x98\x01\n\x13TestNestedExtension29\n\x04test\x12$.protobuf_unittest.TestAllExtensions\x18\xea\x07 \x01(\t:\x04test2F\n\x17nested_string_extension\x12$.protobuf_unittest.TestAllExtensions\x18\xeb\x07 \x01(\t\"\xd5\x05\n\x0cTestRequired\x12\t\n\x01\x61\x18\x01 \x02(\x05\x12\x0e\n\x06\x64ummy2\x18\x02 \x01(\x05\x12\t\n\x01\x62\x18\x03 \x02(\x05\x12\x0e\n\x06\x64ummy4\x18\x04 \x01(\x05\x12\x0e\n\x06\x64ummy5\x18\x05 \x01(\x05\x12\x0e\n\x06\x64ummy6\x18\x06 \x01(\x05\x12\x0e\n\x06\x64ummy7\x18\x07 \x01(\x05\x12\x0e\n\x06\x64ummy8\x18\x08 \x01(\x05\x12\x0e\n\x06\x64ummy9\x18\t \x01(\x05\x12\x0f\n\x07\x64ummy10\x18\n \x01(\x05\x12\x0f\n\x07\x64ummy11\x18\x0b \x01(\x05\x12\x0f\n\x07\x64ummy12\x18\x0c \x01(\x05\x12\x0f\n\x07\x64ummy13\x18\r \x01(\x05\x12\x0f\n\x07\x64ummy14\x18\x0e \x01(\x05\x12\x0f\n\x07\x64ummy15\x18\x0f \x01(\x05\x12\x0f\n\x07\x64ummy16\x18\x10 \x01(\x05\x12\x0f\n\x07\x64ummy17\x18\x11 \x01(\x05\x12\x0f\n\x07\x64ummy18\x18\x12 \x01(\x05\x12\x0f\n\x07\x64ummy19\x18\x13 \x01(\x05\x12\x0f\n\x07\x64ummy20\x18\x14 \x01(\x05\x12\x0f\n\x07\x64ummy21\x18\x15 \x01(\x05\x12\x0f\n\x07\x64ummy22\x18\x16 \x01(\x05\x12\x0f\n\x07\x64ummy23\x18\x17 \x01(\x05\x12\x0f\n\x07\x64ummy24\x18\x18 \x01(\x05\x12\x0f\n\x07\x64ummy25\x18\x19 \x01(\x05\x12\x0f\n\x07\x64ummy26\x18\x1a \x01(\x05\x12\x0f\n\x07\x64ummy27\x18\x1b \x01(\x05\x12\x0f\n\x07\x64ummy28\x18\x1c \x01(\x05\x12\x0f\n\x07\x64ummy29\x18\x1d \x01(\x05\x12\x0f\n\x07\x64ummy30\x18\x1e \x01(\x05\x12\x0f\n\x07\x64ummy31\x18\x1f \x01(\x05\x12\x0f\n\x07\x64ummy32\x18  \x01(\x05\x12\t\n\x01\x63\x18! \x02(\x05\x32V\n\x06single\x12$.protobuf_unittest.TestAllExtensions\x18\xe8\x07 \x01(\x0b\x32\x1f.protobuf_unittest.TestRequired2U\n\x05multi\x12$.protobuf_unittest.TestAllExtensions\x18\xe9\x07 \x03(\x0b\x32\x1f.protobuf_unittest.TestRequired\"\x9a\x01\n\x13TestRequiredForeign\x12\x39\n\x10optional_message\x18\x01 \x01(\x0b\x32\x1f.protobuf_unittest.TestRequired\x12\x39\n\x10repeated_message\x18\x02 \x03(\x0b\x32\x1f.protobuf_unittest.TestRequired\x12\r\n\x05\x64ummy\x18\x03 \x01(\x05\"Z\n\x11TestForeignNested\x12\x45\n\x0e\x66oreign_nested\x18\x01 \x01(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessage\"\x12\n\x10TestEmptyMessage\"*\n\x1eTestEmptyMessageWithExtensions*\x08\x08\x01\x10\x80\x80\x80\x80\x02\"7\n\x1bTestMultipleExtensionRanges*\x04\x08*\x10+*\x06\x08\xaf \x10\x94!*\n\x08\x80\x80\x04\x10\x80\x80\x80\x80\x02\"4\n\x18TestReallyLargeTagNumber\x12\t\n\x01\x61\x18\x01 \x01(\x05\x12\r\n\x02\x62\x62\x18\xff\xff\xff\x7f \x01(\x05\"U\n\x14TestRecursiveMessage\x12\x32\n\x01\x61\x18\x01 \x01(\x0b\x32\'.protobuf_unittest.TestRecursiveMessage\x12\t\n\x01i\x18\x02 \x01(\x05\"K\n\x14TestMutualRecursionA\x12\x33\n\x02\x62\x62\x18\x01 \x01(\x0b\x32\'.protobuf_unittest.TestMutualRecursionB\"b\n\x14TestMutualRecursionB\x12\x32\n\x01\x61\x18\x01 \x01(\x0b\x32\'.protobuf_unittest.TestMutualRecursionA\x12\x16\n\x0eoptional_int32\x18\x02 \x01(\x05\"\xb3\x01\n\x12TestDupFieldNumber\x12\t\n\x01\x61\x18\x01 \x01(\x05\x12\x36\n\x03\x66oo\x18\x02 \x01(\n2).protobuf_unittest.TestDupFieldNumber.Foo\x12\x36\n\x03\x62\x61r\x18\x03 \x01(\n2).protobuf_unittest.TestDupFieldNumber.Bar\x1a\x10\n\x03\x46oo\x12\t\n\x01\x61\x18\x01 \x01(\x05\x1a\x10\n\x03\x42\x61r\x12\t\n\x01\x61\x18\x01 \x01(\x05\"L\n\x10TestEagerMessage\x12\x38\n\x0bsub_message\x18\x01 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypesB\x02(\x00\"K\n\x0fTestLazyMessage\x12\x38\n\x0bsub_message\x18\x01 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypesB\x02(\x01\"\x80\x02\n\x18TestNestedMessageHasBits\x12Z\n\x17optional_nested_message\x18\x01 \x01(\x0b\x32\x39.protobuf_unittest.TestNestedMessageHasBits.NestedMessage\x1a\x87\x01\n\rNestedMessage\x12$\n\x1cnestedmessage_repeated_int32\x18\x01 \x03(\x05\x12P\n%nestedmessage_repeated_foreignmessage\x18\x02 \x03(\x0b\x32!.protobuf_unittest.ForeignMessage\"\xe5\x03\n\x17TestCamelCaseFieldNames\x12\x16\n\x0ePrimitiveField\x18\x01 \x01(\x05\x12\x13\n\x0bStringField\x18\x02 \x01(\t\x12\x31\n\tEnumField\x18\x03 \x01(\x0e\x32\x1e.protobuf_unittest.ForeignEnum\x12\x37\n\x0cMessageField\x18\x04 \x01(\x0b\x32!.protobuf_unittest.ForeignMessage\x12\x1c\n\x10StringPieceField\x18\x05 \x01(\tB\x02\x08\x02\x12\x15\n\tCordField\x18\x06 \x01(\tB\x02\x08\x01\x12\x1e\n\x16RepeatedPrimitiveField\x18\x07 \x03(\x05\x12\x1b\n\x13RepeatedStringField\x18\x08 \x03(\t\x12\x39\n\x11RepeatedEnumField\x18\t \x03(\x0e\x32\x1e.protobuf_unittest.ForeignEnum\x12?\n\x14RepeatedMessageField\x18\n \x03(\x0b\x32!.protobuf_unittest.ForeignMessage\x12$\n\x18RepeatedStringPieceField\x18\x0b \x03(\tB\x02\x08\x02\x12\x1d\n\x11RepeatedCordField\x18\x0c \x03(\tB\x02\x08\x01\"U\n\x12TestFieldOrderings\x12\x11\n\tmy_string\x18\x0b \x01(\t\x12\x0e\n\x06my_int\x18\x01 \x01(\x03\x12\x10\n\x08my_float\x18\x65 \x01(\x02*\x04\x08\x02\x10\x0b*\x04\x08\x0c\x10\x65\"\xb8\x07\n\x18TestExtremeDefaultValues\x12?\n\rescaped_bytes\x18\x01 \x01(\x0c:(\\000\\001\\007\\010\\014\\n\\r\\t\\013\\\\\\\'\\\"\\376\x12 \n\x0clarge_uint32\x18\x02 \x01(\r:\n4294967295\x12*\n\x0clarge_uint64\x18\x03 \x01(\x04:\x14\x31\x38\x34\x34\x36\x37\x34\x34\x30\x37\x33\x37\x30\x39\x35\x35\x31\x36\x31\x35\x12 \n\x0bsmall_int32\x18\x04 \x01(\x05:\x0b-2147483647\x12)\n\x0bsmall_int64\x18\x05 \x01(\x03:\x14-9223372036854775807\x12\'\n\x12really_small_int32\x18\x15 \x01(\x05:\x0b-2147483648\x12\x30\n\x12really_small_int64\x18\x16 \x01(\x03:\x14-9223372036854775808\x12\x18\n\x0butf8_string\x18\x06 \x01(\t:\x03\xe1\x88\xb4\x12\x15\n\nzero_float\x18\x07 \x01(\x02:\x01\x30\x12\x14\n\tone_float\x18\x08 \x01(\x02:\x01\x31\x12\x18\n\x0bsmall_float\x18\t \x01(\x02:\x03\x31.5\x12\x1e\n\x12negative_one_float\x18\n \x01(\x02:\x02-1\x12\x1c\n\x0enegative_float\x18\x0b \x01(\x02:\x04-1.5\x12\x1b\n\x0blarge_float\x18\x0c \x01(\x02:\x06\x32\x65+008\x12%\n\x14small_negative_float\x18\r \x01(\x02:\x07-8e-028\x12\x17\n\ninf_double\x18\x0e \x01(\x01:\x03inf\x12\x1c\n\x0eneg_inf_double\x18\x0f \x01(\x01:\x04-inf\x12\x17\n\nnan_double\x18\x10 \x01(\x01:\x03nan\x12\x16\n\tinf_float\x18\x11 \x01(\x02:\x03inf\x12\x1b\n\rneg_inf_float\x18\x12 \x01(\x02:\x04-inf\x12\x16\n\tnan_float\x18\x13 \x01(\x02:\x03nan\x12+\n\x0c\x63pp_trigraph\x18\x14 \x01(\t:\x15? ? ?? ?? ??? ??/ ??-\x12 \n\x10string_with_zero\x18\x17 \x01(\t:\x06hel\x00lo\x12\"\n\x0f\x62ytes_with_zero\x18\x18 \x01(\x0c:\twor\\000ld\x12(\n\x16string_piece_with_zero\x18\x19 \x01(\t:\x04\x61\x62\x00\x63\x42\x02\x08\x02\x12 \n\x0e\x63ord_with_zero\x18\x1a \x01(\t:\x04\x31\x32\x00\x33\x42\x02\x08\x01\x12&\n\x12replacement_string\x18\x1b \x01(\t:\n${unknown}\"K\n\x11SparseEnumMessage\x12\x36\n\x0bsparse_enum\x18\x01 \x01(\x0e\x32!.protobuf_unittest.TestSparseEnum\"\x19\n\tOneString\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1a\n\nMoreString\x12\x0c\n\x04\x64\x61ta\x18\x01 \x03(\t\"\x18\n\x08OneBytes\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x19\n\tMoreBytes\x12\x0c\n\x04\x64\x61ta\x18\x01 \x03(\x0c\"\x1c\n\x0cInt32Message\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x05\"\x1d\n\rUint32Message\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\r\"\x1c\n\x0cInt64Message\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x03\"\x1d\n\rUint64Message\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x04\"\x1b\n\x0b\x42oolMessage\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x08\"\xd0\x01\n\tTestOneof\x12\x11\n\x07\x66oo_int\x18\x01 \x01(\x05H\x00\x12\x14\n\nfoo_string\x18\x02 \x01(\tH\x00\x12\x36\n\x0b\x66oo_message\x18\x03 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypesH\x00\x12\x39\n\x08\x66oogroup\x18\x04 \x01(\n2%.protobuf_unittest.TestOneof.FooGroupH\x00\x1a \n\x08\x46ooGroup\x12\t\n\x01\x61\x18\x05 \x01(\x05\x12\t\n\x01\x62\x18\x06 \x01(\tB\x05\n\x03\x66oo\"\xe7\x01\n\x1cTestOneofBackwardsCompatible\x12\x0f\n\x07\x66oo_int\x18\x01 \x01(\x05\x12\x12\n\nfoo_string\x18\x02 \x01(\t\x12\x34\n\x0b\x66oo_message\x18\x03 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12J\n\x08\x66oogroup\x18\x04 \x01(\n28.protobuf_unittest.TestOneofBackwardsCompatible.FooGroup\x1a \n\x08\x46ooGroup\x12\t\n\x01\x61\x18\x05 \x01(\x05\x12\t\n\x01\x62\x18\x06 \x01(\t\"\x9e\x06\n\nTestOneof2\x12\x11\n\x07\x66oo_int\x18\x01 \x01(\x05H\x00\x12\x14\n\nfoo_string\x18\x02 \x01(\tH\x00\x12\x16\n\x08\x66oo_cord\x18\x03 \x01(\tB\x02\x08\x01H\x00\x12\x1e\n\x10\x66oo_string_piece\x18\x04 \x01(\tB\x02\x08\x02H\x00\x12\x13\n\tfoo_bytes\x18\x05 \x01(\x0cH\x00\x12<\n\x08\x66oo_enum\x18\x06 \x01(\x0e\x32(.protobuf_unittest.TestOneof2.NestedEnumH\x00\x12\x42\n\x0b\x66oo_message\x18\x07 \x01(\x0b\x32+.protobuf_unittest.TestOneof2.NestedMessageH\x00\x12:\n\x08\x66oogroup\x18\x08 \x01(\n2&.protobuf_unittest.TestOneof2.FooGroupH\x00\x12K\n\x10\x66oo_lazy_message\x18\x0b \x01(\x0b\x32+.protobuf_unittest.TestOneof2.NestedMessageB\x02(\x01H\x00\x12\x14\n\x07\x62\x61r_int\x18\x0c \x01(\x05:\x01\x35H\x01\x12\x1c\n\nbar_string\x18\r \x01(\t:\x06STRINGH\x01\x12\x1c\n\x08\x62\x61r_cord\x18\x0e \x01(\t:\x04\x43ORDB\x02\x08\x01H\x01\x12&\n\x10\x62\x61r_string_piece\x18\x0f \x01(\t:\x06SPIECEB\x02\x08\x02H\x01\x12\x1a\n\tbar_bytes\x18\x10 \x01(\x0c:\x05\x42YTESH\x01\x12\x41\n\x08\x62\x61r_enum\x18\x11 \x01(\x0e\x32(.protobuf_unittest.TestOneof2.NestedEnum:\x03\x42\x41RH\x01\x12\x0f\n\x07\x62\x61z_int\x18\x12 \x01(\x05\x12\x17\n\nbaz_string\x18\x13 \x01(\t:\x03\x42\x41Z\x1a \n\x08\x46ooGroup\x12\t\n\x01\x61\x18\t \x01(\x05\x12\t\n\x01\x62\x18\n \x01(\t\x1a\x33\n\rNestedMessage\x12\x0f\n\x07qux_int\x18\x01 \x01(\x03\x12\x11\n\tcorge_int\x18\x02 \x03(\x05\"\'\n\nNestedEnum\x12\x07\n\x03\x46OO\x10\x01\x12\x07\n\x03\x42\x41R\x10\x02\x12\x07\n\x03\x42\x41Z\x10\x03\x42\x05\n\x03\x66ooB\x05\n\x03\x62\x61r\"\xb8\x01\n\x11TestRequiredOneof\x12\x11\n\x07\x66oo_int\x18\x01 \x01(\x05H\x00\x12\x14\n\nfoo_string\x18\x02 \x01(\tH\x00\x12I\n\x0b\x66oo_message\x18\x03 \x01(\x0b\x32\x32.protobuf_unittest.TestRequiredOneof.NestedMessageH\x00\x1a(\n\rNestedMessage\x12\x17\n\x0frequired_double\x18\x01 \x02(\x01\x42\x05\n\x03\x66oo\"\xaa\x03\n\x0fTestPackedTypes\x12\x18\n\x0cpacked_int32\x18Z \x03(\x05\x42\x02\x10\x01\x12\x18\n\x0cpacked_int64\x18[ \x03(\x03\x42\x02\x10\x01\x12\x19\n\rpacked_uint32\x18\\ \x03(\rB\x02\x10\x01\x12\x19\n\rpacked_uint64\x18] \x03(\x04\x42\x02\x10\x01\x12\x19\n\rpacked_sint32\x18^ \x03(\x11\x42\x02\x10\x01\x12\x19\n\rpacked_sint64\x18_ \x03(\x12\x42\x02\x10\x01\x12\x1a\n\x0epacked_fixed32\x18` \x03(\x07\x42\x02\x10\x01\x12\x1a\n\x0epacked_fixed64\x18\x61 \x03(\x06\x42\x02\x10\x01\x12\x1b\n\x0fpacked_sfixed32\x18\x62 \x03(\x0f\x42\x02\x10\x01\x12\x1b\n\x0fpacked_sfixed64\x18\x63 \x03(\x10\x42\x02\x10\x01\x12\x18\n\x0cpacked_float\x18\x64 \x03(\x02\x42\x02\x10\x01\x12\x19\n\rpacked_double\x18\x65 \x03(\x01\x42\x02\x10\x01\x12\x17\n\x0bpacked_bool\x18\x66 \x03(\x08\x42\x02\x10\x01\x12\x37\n\x0bpacked_enum\x18g \x03(\x0e\x32\x1e.protobuf_unittest.ForeignEnumB\x02\x10\x01\"\xc8\x03\n\x11TestUnpackedTypes\x12\x1a\n\x0eunpacked_int32\x18Z \x03(\x05\x42\x02\x10\x00\x12\x1a\n\x0eunpacked_int64\x18[ \x03(\x03\x42\x02\x10\x00\x12\x1b\n\x0funpacked_uint32\x18\\ \x03(\rB\x02\x10\x00\x12\x1b\n\x0funpacked_uint64\x18] \x03(\x04\x42\x02\x10\x00\x12\x1b\n\x0funpacked_sint32\x18^ \x03(\x11\x42\x02\x10\x00\x12\x1b\n\x0funpacked_sint64\x18_ \x03(\x12\x42\x02\x10\x00\x12\x1c\n\x10unpacked_fixed32\x18` \x03(\x07\x42\x02\x10\x00\x12\x1c\n\x10unpacked_fixed64\x18\x61 \x03(\x06\x42\x02\x10\x00\x12\x1d\n\x11unpacked_sfixed32\x18\x62 \x03(\x0f\x42\x02\x10\x00\x12\x1d\n\x11unpacked_sfixed64\x18\x63 \x03(\x10\x42\x02\x10\x00\x12\x1a\n\x0eunpacked_float\x18\x64 \x03(\x02\x42\x02\x10\x00\x12\x1b\n\x0funpacked_double\x18\x65 \x03(\x01\x42\x02\x10\x00\x12\x19\n\runpacked_bool\x18\x66 \x03(\x08\x42\x02\x10\x00\x12\x39\n\runpacked_enum\x18g \x03(\x0e\x32\x1e.protobuf_unittest.ForeignEnumB\x02\x10\x00\" \n\x14TestPackedExtensions*\x08\x08\x01\x10\x80\x80\x80\x80\x02\"\"\n\x16TestUnpackedExtensions*\x08\x08\x01\x10\x80\x80\x80\x80\x02\"\x99\x04\n\x15TestDynamicExtensions\x12\x19\n\x10scalar_extension\x18\xd0\x0f \x01(\x07\x12\x37\n\x0e\x65num_extension\x18\xd1\x0f \x01(\x0e\x32\x1e.protobuf_unittest.ForeignEnum\x12Y\n\x16\x64ynamic_enum_extension\x18\xd2\x0f \x01(\x0e\x32\x38.protobuf_unittest.TestDynamicExtensions.DynamicEnumType\x12=\n\x11message_extension\x18\xd3\x0f \x01(\x0b\x32!.protobuf_unittest.ForeignMessage\x12_\n\x19\x64ynamic_message_extension\x18\xd4\x0f \x01(\x0b\x32;.protobuf_unittest.TestDynamicExtensions.DynamicMessageType\x12\x1b\n\x12repeated_extension\x18\xd5\x0f \x03(\t\x12\x1d\n\x10packed_extension\x18\xd6\x0f \x03(\x11\x42\x02\x10\x01\x1a,\n\x12\x44ynamicMessageType\x12\x16\n\rdynamic_field\x18\xb4\x10 \x01(\x05\"G\n\x0f\x44ynamicEnumType\x12\x10\n\x0b\x44YNAMIC_FOO\x10\x98\x11\x12\x10\n\x0b\x44YNAMIC_BAR\x10\x99\x11\x12\x10\n\x0b\x44YNAMIC_BAZ\x10\x9a\x11\"\xc0\x01\n"\xf7\t\n\x10TestParsingMerge\x12;\n\x12required_all_types\x18\x01 \x02(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12;\n\x12optional_all_types\x18\x02 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12;\n\x12repeated_all_types\x18\x03 \x03(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12H\n\roptionalgroup\x18\n \x01(\n21.protobuf_unittest.TestParsingMerge.OptionalGroup\x12H\n\rrepeatedgroup\x18\x14 \x03(\n21.protobuf_unittest.TestParsingMerge.RepeatedGroup\x1a\xaa\x04\n\x17RepeatedFieldsGenerator\x12/\n\x06\x66ield1\x18\x01 \x03(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12/\n\x06\x66ield2\x18\x02 \x03(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12/\n\x06\x66ield3\x18\x03 \x03(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12R\n\x06group1\x18\n \x03(\n2B.protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.Group1\x12R\n\x06group2\x18\x14 \x03(\n2B.protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.Group2\x12.\n\x04\x65xt1\x18\xe8\x07 \x03(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x12.\n\x04\x65xt2\x18\xe9\x07 \x03(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x1a\x39\n\x06Group1\x12/\n\x06\x66ield1\x18\x0b \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x1a\x39\n\x06Group2\x12/\n\x06\x66ield1\x18\x15 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x1aR\n\rOptionalGroup\x12\x41\n\x18optional_group_all_types\x18\x0b \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes\x1aR\n\rRepeatedGroup\x12\x41\n\x18repeated_group_all_types\x18\x15 \x01(\x0b\x32\x1f.protobuf_unittest.TestAllTypes*\t\x08\xe8\x07\x10\x80\x80\x80\x80\x02\x32[\n\x0coptional_ext\x12"D\n\x1bTestCommentInjectionMessage\x12%\n\x01\x61\x18\x01 \x01(\t:\x1a*/ <- Neither should this.\"\x0c\n\nFooRequest\"\r\n\x0b\x46ooResponse\"\x12\n\x10\x46ooClientMessage\"\x12\n\x10\x46ooServerMessage\"\x0c\n\nBarRequest\"\r\n\x0b\x42\x61rResponse*@\n\x0b\x46oreignEnum\x12\x0f\n\x0b\x46OREIGN_FOO\x10\x04\x12\x0f\n\x0b\x46OREIGN_BAR\x10\x05\x12\x0f\n\x0b\x46OREIGN_BAZ\x10\x06*K\n\x14TestEnumWithDupValue\x12\x08\n\x04\x46OO1\x10\x01\x12\x08\n\x04\x42\x41R1\x10\x02\x12\x07\n\x03\x42\x41Z\x10\x03\x12\x08\n\x04\x46OO2\x10\x01\x12\x08\n\x04\x42\x41R2\x10\x02\x1a\x02\x10\x01*\x89\x01\n\x0eTestSparseEnum\x12\x0c\n\x08SPARSE_A\x10{\x12\x0e\n\x08SPARSE_B\x10\xa6\xe7\x03\x12\x0f\n\x08SPARSE_C\x10\xb2\xb1\x80\x06\x12\x15\n\x08SPARSE_D\x10\xf1\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x15\n\x08SPARSE_E\x10\xb4\xde\xfc\xff\xff\xff\xff\xff\xff\x01\x12\x0c\n\x08SPARSE_F\x10\x00\x12\x0c\n\x08SPARSE_G\x10\x02\x32\x99\x01\n\x0bTestService\x12\x44\n\x03\x46oo\x12\x1d.protobuf_unittest.FooRequest\x1a\x1e.protobuf_unittest.FooResponse\x12\x44\n\x03\x42\x61r\x12\x1d.protobuf_unittest.BarRequest\x1a\x1e.protobuf_unittest.BarResponse:F\n\x18optional_int32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x01 \x01(\x05:F\n\x18optional_int64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x02 \x01(\x03:G\n\x19optional_uint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x03 \x01(\r:G\n\x19optional_uint64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x04 \x01(\x04:G\n\x19optional_sint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x05 \x01(\x11:G\n\x19optional_sint64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x06 \x01(\x12:H\n\x1aoptional_fixed32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x07 \x01(\x07:H\n\x1aoptional_fixed64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x08 \x01(\x06:I\n\x1boptional_sfixed32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\t \x01(\x0f:I\n\x1boptional_sfixed64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\n \x01(\x10:F\n\x18optional_float_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x0b \x01(\x02:G\n\x19optional_double_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x0c \x01(\x01:E\n\x17optional_bool_extension\x12$.protobuf_unittest.TestAllExtensions\x18\r \x01(\x08:G\n\x19optional_string_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x0e \x01(\t:F\n\x18optional_bytes_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x0f \x01(\x0c:q\n\x17optionalgroup_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x10 \x01(\n2*.protobuf_unittest.OptionalGroup_extension:~\n!optional_nested_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x12 \x01(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessage:s\n\"optional_foreign_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x13 \x01(\x0b\x32!.protobuf_unittest.ForeignMessage:x\n!optional_import_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x14 \x01(\x0b\x32\'.protobuf_unittest_import.ImportMessage:x\n\x1eoptional_nested_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x15 \x01(\x0e\x32*.protobuf_unittest.TestAllTypes.NestedEnum:m\n\x1foptional_foreign_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x16 \x01(\x0e\x32\x1e.protobuf_unittest.ForeignEnum:r\n\x1eoptional_import_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x17 \x01(\x0e\x32$.protobuf_unittest_import.ImportEnum:Q\n\x1foptional_string_piece_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x18 \x01(\tB\x02\x08\x02:I\n\x17optional_cord_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x19 \x01(\tB\x02\x08\x01:\x85\x01\n(optional_public_import_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x1a \x01(\x0b\x32-.protobuf_unittest_import.PublicImportMessage:\x80\x01\n\x1foptional_lazy_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x1b \x01(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessageB\x02(\x01:F\n\x18repeated_int32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x1f \x03(\x05:F\n\x18repeated_int64_extension\x12$.protobuf_unittest.TestAllExtensions\x18  \x03(\x03:G\n\x19repeated_uint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18! \x03(\r:G\n\x19repeated_uint64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\" \x03(\x04:G\n\x19repeated_sint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18"repeated_foreign_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x31 \x03(\x0b\x32!.protobuf_unittest.ForeignMessage:x\n!repeated_import_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x32 \x03(\x0b\x32\'.protobuf_unittest_import.ImportMessage:x\n\x1erepeated_nested_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x33 \x03(\x0e\x32*.protobuf_unittest.TestAllTypes.NestedEnum:m\n\x1frepeated_foreign_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x34 \x03(\x0e\x32\x1e.protobuf_unittest.ForeignEnum:r\n\x1erepeated_import_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x35 \x03(\x0e\x32$.protobuf_unittest_import.ImportEnum:Q\n\x1frepeated_string_piece_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x36 \x03(\tB\x02\x08\x02:I\n\x17repeated_cord_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x37 \x03(\tB\x02\x08\x01:\x80\x01\n\x1frepeated_lazy_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x39 \x03(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessageB\x02(\x01:I\n\x17\x64\x65\x66\x61ult_int32_extension\x12$.protobuf_unittest.TestAllExtensions\x18= \x01(\x05:\x02\x34\x31:I\n\x17\x64\x65\x66\x61ult_int64_extension\x12$.protobuf_unittest.TestAllExtensions\x18> \x01(\x03:\x02\x34\x32:J\n\x18\x64\x65\x66\x61ult_uint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18? \x01(\r:\x02\x34\x33:J\n\x18\x64\x65\x66\x61ult_uint64_extension\x12$.protobuf_unittest.TestAllExtensions\x18@ \x01(\x04:\x02\x34\x34:K\n\x18\x64\x65\x66\x61ult_sint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x41 \x01(\x11:\x03-45:J\n\x18\x64\x65\x66\x61ult_sint64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x42 \x01(\x12:\x02\x34\x36:K\n\x19\x64\x65\x66\x61ult_fixed32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x43 \x01(\x07:\x02\x34\x37:K\n\x19\x64\x65\x66\x61ult_fixed64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x44 \x01(\x06:\x02\x34\x38:L\n\x1a\x64\x65\x66\x61ult_sfixed32_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x45 \x01(\x0f:\x02\x34\x39:M\n\x1a\x64\x65\x66\x61ult_sfixed64_extension\x12$.protobuf_unittest.TestAllExtensions\x18\x46 \x01(\x10:\x03-50:K\n\x17\x64\x65\x66\x61ult_float_extension\x12$.protobuf_unittest.TestAllExtensions\x18G \x01(\x02:\x04\x35\x31.5:M\n\x18\x64\x65\x66\x61ult_double_extension\x12$.protobuf_unittest.TestAllExtensions\x18H \x01(\x01:\x05\x35\x32\x30\x30\x30:J\n\x16\x64\x65\x66\x61ult_bool_extension\x12$.protobuf_unittest.TestAllExtensions\x18I \x01(\x08:\x04true:M\n\x18\x64\x65\x66\x61ult_string_extension\x12$.protobuf_unittest.TestAllExtensions\x18J \x01(\t:\x05hello:L\n\x17\x64\x65\x66\x61ult_bytes_extension\x12$.protobuf_unittest.TestAllExtensions\x18K \x01(\x0c:\x05world:|\n\x1d\x64\x65\x66\x61ult_nested_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18Q \x01(\x0e\x32*.protobuf_unittest.TestAllTypes.NestedEnum:\x03\x42\x41R:y\n\x1e\x64\x65\x66\x61ult_foreign_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18R \x01(\x0e\x32\x1e.protobuf_unittest.ForeignEnum:\x0b\x46OREIGN_BAR:}\n\x1d\x64\x65\x66\x61ult_import_enum_extension\x12$.protobuf_unittest.TestAllExtensions\x18S \x01(\x0e\x32$.protobuf_unittest_import.ImportEnum:\nIMPORT_BAR:U\n\x1e\x64\x65\x66\x61ult_string_piece_extension\x12$.protobuf_unittest.TestAllExtensions\x18T \x01(\t:\x03\x61\x62\x63\x42\x02\x08\x02:M\n\x16\x64\x65\x66\x61ult_cord_extension\x12$.protobuf_unittest.TestAllExtensions\x18U \x01(\t:\x03\x31\x32\x33\x42\x02\x08\x01:D\n\x16oneof_uint32_extension\x12$.protobuf_unittest.TestAllExtensions\x18o \x01(\r:{\n\x1eoneof_nested_message_extension\x12$.protobuf_unittest.TestAllExtensions\x18p \x01(\x0b\x32-.protobuf_unittest.TestAllTypes.NestedMessage:D\n\x16oneof_string_extension\x12$.protobuf_unittest.TestAllExtensions\x18q \x01(\t:C\n\x15oneof_bytes_extension\x12$.protobuf_unittest.TestAllExtensions\x18r \x01(\x0c:B\n\x13my_extension_string\x12%.protobuf_unittest.TestFieldOrderings\x18\x32 \x01(\t:?\n\x10my_extension_int\x12%.protobuf_unittest.TestFieldOrderings\x18\x05 \x01(\x05:K\n\x16packed_int32_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18Z \x03(\x05\x42\x02\x10\x01:K\n\x16packed_int64_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18[ \x03(\x03\x42\x02\x10\x01:L\n\x17packed_uint32_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\\ \x03(\rB\x02\x10\x01:L\n\x17packed_uint64_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18] \x03(\x04\x42\x02\x10\x01:L\n\x17packed_sint32_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18^ \x03(\x11\x42\x02\x10\x01:L\n\x17packed_sint64_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18_ \x03(\x12\x42\x02\x10\x01:M\n\x18packed_fixed32_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18` \x03(\x07\x42\x02\x10\x01:M\n\x18packed_fixed64_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\x61 \x03(\x06\x42\x02\x10\x01:N\n\x19packed_sfixed32_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\x62 \x03(\x0f\x42\x02\x10\x01:N\n\x19packed_sfixed64_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\x63 \x03(\x10\x42\x02\x10\x01:K\n\x16packed_float_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\x64 \x03(\x02\x42\x02\x10\x01:L\n\x17packed_double_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\x65 \x03(\x01\x42\x02\x10\x01:J\n\x15packed_bool_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18\x66 \x03(\x08\x42\x02\x10\x01:j\n\x15packed_enum_extension\x12\'.protobuf_unittest.TestPackedExtensions\x18g \x03(\x0e\x32\x1e.protobuf_unittest.ForeignEnumB\x02\x10\x01:O\n\x18unpacked_int32_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18Z \x03(\x05\x42\x02\x10\x00:O\n\x18unpacked_int64_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18[ \x03(\x03\x42\x02\x10\x00:P\n\x19unpacked_uint32_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\\ \x03(\rB\x02\x10\x00:P\n\x19unpacked_uint64_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18] \x03(\x04\x42\x02\x10\x00:P\n\x19unpacked_sint32_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18^ \x03(\x11\x42\x02\x10\x00:P\n\x19unpacked_sint64_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18_ \x03(\x12\x42\x02\x10\x00:Q\n\x1aunpacked_fixed32_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18` \x03(\x07\x42\x02\x10\x00:Q\n\x1aunpacked_fixed64_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\x61 \x03(\x06\x42\x02\x10\x00:R\n\x1bunpacked_sfixed32_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\x62 \x03(\x0f\x42\x02\x10\x00:R\n\x1bunpacked_sfixed64_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\x63 \x03(\x10\x42\x02\x10\x00:O\n\x18unpacked_float_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\x64 \x03(\x02\x42\x02\x10\x00:P\n\x19unpacked_double_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\x65 \x03(\x01\x42\x02\x10\x00:N\n\x17unpacked_bool_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18\x66 \x03(\x08\x42\x02\x10\x00:n\n\x17unpacked_enum_extension\x12).protobuf_unittest.TestUnpackedExtensions\x18g \x03(\x0e\x32\x1e.protobuf_unittest.ForeignEnumB\x02\x10\x00\x42\x1a\x42\rUnittestProtoH\x01\x80\x01\x01\x88\x01\x01\x90\x01\x01')
  ,
  dependencies=[google.protobuf.unittest_import_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_FOREIGNENUM = _descriptor.EnumDescriptor(
  name='ForeignEnum',
  full_name='protobuf_unittest.ForeignEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FOREIGN_FOO', index=0, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FOREIGN_BAR', index=1, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FOREIGN_BAZ', index=2, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=12193,
  serialized_end=12257,
)
_sym_db.RegisterEnumDescriptor(_FOREIGNENUM)

ForeignEnum = enum_type_wrapper.EnumTypeWrapper(_FOREIGNENUM)
_TESTENUMWITHDUPVALUE = _descriptor.EnumDescriptor(
  name='TestEnumWithDupValue',
  full_name='protobuf_unittest.TestEnumWithDupValue',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FOO1', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAR1', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAZ', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FOO2', index=3, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAR2', index=4, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=_descriptor._ParseOptions(descriptor_pb2.EnumOptions(), _b('\020\001')),
  serialized_start=12259,
  serialized_end=12334,
)
_sym_db.RegisterEnumDescriptor(_TESTENUMWITHDUPVALUE)

TestEnumWithDupValue = enum_type_wrapper.EnumTypeWrapper(_TESTENUMWITHDUPVALUE)
_TESTSPARSEENUM = _descriptor.EnumDescriptor(
  name='TestSparseEnum',
  full_name='protobuf_unittest.TestSparseEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SPARSE_A', index=0, number=123,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_B', index=1, number=62374,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_C', index=2, number=12589234,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_D', index=3, number=-15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_E', index=4, number=-53452,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_F', index=5, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_G', index=6, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=12337,
  serialized_end=12474,
)
_sym_db.RegisterEnumDescriptor(_TESTSPARSEENUM)

TestSparseEnum = enum_type_wrapper.EnumTypeWrapper(_TESTSPARSEENUM)
FOREIGN_FOO = 4
FOREIGN_BAR = 5
FOREIGN_BAZ = 6
FOO1 = 1
BAR1 = 2
BAZ = 3
FOO2 = 1
BAR2 = 2
SPARSE_A = 123
SPARSE_B = 62374
SPARSE_C = 12589234
SPARSE_D = -15
SPARSE_E = -53452
SPARSE_F = 0
SPARSE_G = 2

OPTIONAL_INT32_EXTENSION_FIELD_NUMBER = 1
optional_int32_extension = _descriptor.FieldDescriptor(
  name='optional_int32_extension', full_name='protobuf_unittest.optional_int32_extension', index=0,
  number=1, type=5, cpp_type=1, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_INT64_EXTENSION_FIELD_NUMBER = 2
optional_int64_extension = _descriptor.FieldDescriptor(
  name='optional_int64_extension', full_name='protobuf_unittest.optional_int64_extension', index=1,
  number=2, type=3, cpp_type=2, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_UINT32_EXTENSION_FIELD_NUMBER = 3
optional_uint32_extension = _descriptor.FieldDescriptor(
  name='optional_uint32_extension', full_name='protobuf_unittest.optional_uint32_extension', index=2,
  number=3, type=13, cpp_type=3, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_UINT64_EXTENSION_FIELD_NUMBER = 4
optional_uint64_extension = _descriptor.FieldDescriptor(
  name='optional_uint64_extension', full_name='protobuf_unittest.optional_uint64_extension', index=3,
  number=4, type=4, cpp_type=4, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_SINT32_EXTENSION_FIELD_NUMBER = 5
optional_sint32_extension = _descriptor.FieldDescriptor(
  name='optional_sint32_extension', full_name='protobuf_unittest.optional_sint32_extension', index=4,
  number=5, type=17, cpp_type=1, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_SINT64_EXTENSION_FIELD_NUMBER = 6
optional_sint64_extension = _descriptor.FieldDescriptor(
  name='optional_sint64_extension', full_name='protobuf_unittest.optional_sint64_extension', index=5,
  number=6, type=18, cpp_type=2, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_FIXED32_EXTENSION_FIELD_NUMBER = 7
optional_fixed32_extension = _descriptor.FieldDescriptor(
  name='optional_fixed32_extension', full_name='protobuf_unittest.optional_fixed32_extension', index=6,
  number=7, type=7, cpp_type=3, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_FIXED64_EXTENSION_FIELD_NUMBER = 8
optional_fixed64_extension = _descriptor.FieldDescriptor(
  name='optional_fixed64_extension', full_name='protobuf_unittest.optional_fixed64_extension', index=7,
  number=8, type=6, cpp_type=4, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_SFIXED32_EXTENSION_FIELD_NUMBER = 9
optional_sfixed32_extension = _descriptor.FieldDescriptor(
  name='optional_sfixed32_extension', full_name='protobuf_unittest.optional_sfixed32_extension', index=8,
  number=9, type=15, cpp_type=1, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_SFIXED64_EXTENSION_FIELD_NUMBER = 10
optional_sfixed64_extension = _descriptor.FieldDescriptor(
  name='optional_sfixed64_extension', full_name='protobuf_unittest.optional_sfixed64_extension', index=9,
  number=10, type=16, cpp_type=2, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_FLOAT_EXTENSION_FIELD_NUMBER = 11
optional_float_extension = _descriptor.FieldDescriptor(
  name='optional_float_extension', full_name='protobuf_unittest.optional_float_extension', index=10,
  number=11, type=2, cpp_type=6, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_DOUBLE_EXTENSION_FIELD_NUMBER = 12
optional_double_extension = _descriptor.FieldDescriptor(
  name='optional_double_extension', full_name='protobuf_unittest.optional_double_extension', index=11,
  number=12, type=1, cpp_type=5, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_BOOL_EXTENSION_FIELD_NUMBER = 13
optional_bool_extension = _descriptor.FieldDescriptor(
  name='optional_bool_extension', full_name='protobuf_unittest.optional_bool_extension', index=12,
  number=13, type=8, cpp_type=7, label=1,
  has_default_value=False, default_value=False,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_STRING_EXTENSION_FIELD_NUMBER = 14
optional_string_extension = _descriptor.FieldDescriptor(
  name='optional_string_extension', full_name='protobuf_unittest.optional_string_extension', index=13,
  number=14, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=_b("").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_BYTES_EXTENSION_FIELD_NUMBER = 15
optional_bytes_extension = _descriptor.FieldDescriptor(
  name='optional_bytes_extension', full_name='protobuf_unittest.optional_bytes_extension', index=14,
  number=15, type=12, cpp_type=9, label=1,
  has_default_value=False, default_value=_b(""),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONALGROUP_EXTENSION_FIELD_NUMBER = 16
optionalgroup_extension = _descriptor.FieldDescriptor(
  name='optionalgroup_extension', full_name='protobuf_unittest.optionalgroup_extension', index=15,
  number=16, type=10, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_NESTED_MESSAGE_EXTENSION_FIELD_NUMBER = 18
optional_nested_message_extension = _descriptor.FieldDescriptor(
  name='optional_nested_message_extension', full_name='protobuf_unittest.optional_nested_message_extension', index=16,
  number=18, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_FOREIGN_MESSAGE_EXTENSION_FIELD_NUMBER = 19
optional_foreign_message_extension = _descriptor.FieldDescriptor(
  name='optional_foreign_message_extension', full_name='protobuf_unittest.optional_foreign_message_extension', index=17,
  number=19, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_IMPORT_MESSAGE_EXTENSION_FIELD_NUMBER = 20
optional_import_message_extension = _descriptor.FieldDescriptor(
  name='optional_import_message_extension', full_name='protobuf_unittest.optional_import_message_extension', index=18,
  number=20, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_NESTED_ENUM_EXTENSION_FIELD_NUMBER = 21
optional_nested_enum_extension = _descriptor.FieldDescriptor(
  name='optional_nested_enum_extension', full_name='protobuf_unittest.optional_nested_enum_extension', index=19,
  number=21, type=14, cpp_type=8, label=1,
  has_default_value=False, default_value=1,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_FOREIGN_ENUM_EXTENSION_FIELD_NUMBER = 22
optional_foreign_enum_extension = _descriptor.FieldDescriptor(
  name='optional_foreign_enum_extension', full_name='protobuf_unittest.optional_foreign_enum_extension', index=20,
  number=22, type=14, cpp_type=8, label=1,
  has_default_value=False, default_value=4,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_IMPORT_ENUM_EXTENSION_FIELD_NUMBER = 23
optional_import_enum_extension = _descriptor.FieldDescriptor(
  name='optional_import_enum_extension', full_name='protobuf_unittest.optional_import_enum_extension', index=21,
  number=23, type=14, cpp_type=8, label=1,
  has_default_value=False, default_value=7,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_STRING_PIECE_EXTENSION_FIELD_NUMBER = 24
optional_string_piece_extension = _descriptor.FieldDescriptor(
  name='optional_string_piece_extension', full_name='protobuf_unittest.optional_string_piece_extension', index=22,
  number=24, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=_b("").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002')))
OPTIONAL_CORD_EXTENSION_FIELD_NUMBER = 25
optional_cord_extension = _descriptor.FieldDescriptor(
  name='optional_cord_extension', full_name='protobuf_unittest.optional_cord_extension', index=23,
  number=25, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=_b("").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001')))
OPTIONAL_PUBLIC_IMPORT_MESSAGE_EXTENSION_FIELD_NUMBER = 26
optional_public_import_message_extension = _descriptor.FieldDescriptor(
  name='optional_public_import_message_extension', full_name='protobuf_unittest.optional_public_import_message_extension', index=24,
  number=26, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
OPTIONAL_LAZY_MESSAGE_EXTENSION_FIELD_NUMBER = 27
optional_lazy_message_extension = _descriptor.FieldDescriptor(
  name='optional_lazy_message_extension', full_name='protobuf_unittest.optional_lazy_message_extension', index=25,
  number=27, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001')))
REPEATED_INT32_EXTENSION_FIELD_NUMBER = 31
repeated_int32_extension = _descriptor.FieldDescriptor(
  name='repeated_int32_extension', full_name='protobuf_unittest.repeated_int32_extension', index=26,
  number=31, type=5, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_INT64_EXTENSION_FIELD_NUMBER = 32
repeated_int64_extension = _descriptor.FieldDescriptor(
  name='repeated_int64_extension', full_name='protobuf_unittest.repeated_int64_extension', index=27,
  number=32, type=3, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_UINT32_EXTENSION_FIELD_NUMBER = 33
repeated_uint32_extension = _descriptor.FieldDescriptor(
  name='repeated_uint32_extension', full_name='protobuf_unittest.repeated_uint32_extension', index=28,
  number=33, type=13, cpp_type=3, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_UINT64_EXTENSION_FIELD_NUMBER = 34
repeated_uint64_extension = _descriptor.FieldDescriptor(
  name='repeated_uint64_extension', full_name='protobuf_unittest.repeated_uint64_extension', index=29,
  number=34, type=4, cpp_type=4, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_SINT32_EXTENSION_FIELD_NUMBER = 35
repeated_sint32_extension = _descriptor.FieldDescriptor(
  name='repeated_sint32_extension', full_name='protobuf_unittest.repeated_sint32_extension', index=30,
  number=35, type=17, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_SINT64_EXTENSION_FIELD_NUMBER = 36
repeated_sint64_extension = _descriptor.FieldDescriptor(
  name='repeated_sint64_extension', full_name='protobuf_unittest.repeated_sint64_extension', index=31,
  number=36, type=18, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_FIXED32_EXTENSION_FIELD_NUMBER = 37
repeated_fixed32_extension = _descriptor.FieldDescriptor(
  name='repeated_fixed32_extension', full_name='protobuf_unittest.repeated_fixed32_extension', index=32,
  number=37, type=7, cpp_type=3, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_FIXED64_EXTENSION_FIELD_NUMBER = 38
repeated_fixed64_extension = _descriptor.FieldDescriptor(
  name='repeated_fixed64_extension', full_name='protobuf_unittest.repeated_fixed64_extension', index=33,
  number=38, type=6, cpp_type=4, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_SFIXED32_EXTENSION_FIELD_NUMBER = 39
repeated_sfixed32_extension = _descriptor.FieldDescriptor(
  name='repeated_sfixed32_extension', full_name='protobuf_unittest.repeated_sfixed32_extension', index=34,
  number=39, type=15, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_SFIXED64_EXTENSION_FIELD_NUMBER = 40
repeated_sfixed64_extension = _descriptor.FieldDescriptor(
  name='repeated_sfixed64_extension', full_name='protobuf_unittest.repeated_sfixed64_extension', index=35,
  number=40, type=16, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_FLOAT_EXTENSION_FIELD_NUMBER = 41
repeated_float_extension = _descriptor.FieldDescriptor(
  name='repeated_float_extension', full_name='protobuf_unittest.repeated_float_extension', index=36,
  number=41, type=2, cpp_type=6, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_DOUBLE_EXTENSION_FIELD_NUMBER = 42
repeated_double_extension = _descriptor.FieldDescriptor(
  name='repeated_double_extension', full_name='protobuf_unittest.repeated_double_extension', index=37,
  number=42, type=1, cpp_type=5, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_BOOL_EXTENSION_FIELD_NUMBER = 43
repeated_bool_extension = _descriptor.FieldDescriptor(
  name='repeated_bool_extension', full_name='protobuf_unittest.repeated_bool_extension', index=38,
  number=43, type=8, cpp_type=7, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_STRING_EXTENSION_FIELD_NUMBER = 44
repeated_string_extension = _descriptor.FieldDescriptor(
  name='repeated_string_extension', full_name='protobuf_unittest.repeated_string_extension', index=39,
  number=44, type=9, cpp_type=9, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_BYTES_EXTENSION_FIELD_NUMBER = 45
repeated_bytes_extension = _descriptor.FieldDescriptor(
  name='repeated_bytes_extension', full_name='protobuf_unittest.repeated_bytes_extension', index=40,
  number=45, type=12, cpp_type=9, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATEDGROUP_EXTENSION_FIELD_NUMBER = 46
repeatedgroup_extension = _descriptor.FieldDescriptor(
  name='repeatedgroup_extension', full_name='protobuf_unittest.repeatedgroup_extension', index=41,
  number=46, type=10, cpp_type=10, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_NESTED_MESSAGE_EXTENSION_FIELD_NUMBER = 48
repeated_nested_message_extension = _descriptor.FieldDescriptor(
  name='repeated_nested_message_extension', full_name='protobuf_unittest.repeated_nested_message_extension', index=42,
  number=48, type=11, cpp_type=10, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_FOREIGN_MESSAGE_EXTENSION_FIELD_NUMBER = 49
repeated_foreign_message_extension = _descriptor.FieldDescriptor(
  name='repeated_foreign_message_extension', full_name='protobuf_unittest.repeated_foreign_message_extension', index=43,
  number=49, type=11, cpp_type=10, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_IMPORT_MESSAGE_EXTENSION_FIELD_NUMBER = 50
repeated_import_message_extension = _descriptor.FieldDescriptor(
  name='repeated_import_message_extension', full_name='protobuf_unittest.repeated_import_message_extension', index=44,
  number=50, type=11, cpp_type=10, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_NESTED_ENUM_EXTENSION_FIELD_NUMBER = 51
repeated_nested_enum_extension = _descriptor.FieldDescriptor(
  name='repeated_nested_enum_extension', full_name='protobuf_unittest.repeated_nested_enum_extension', index=45,
  number=51, type=14, cpp_type=8, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_FOREIGN_ENUM_EXTENSION_FIELD_NUMBER = 52
repeated_foreign_enum_extension = _descriptor.FieldDescriptor(
  name='repeated_foreign_enum_extension', full_name='protobuf_unittest.repeated_foreign_enum_extension', index=46,
  number=52, type=14, cpp_type=8, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_IMPORT_ENUM_EXTENSION_FIELD_NUMBER = 53
repeated_import_enum_extension = _descriptor.FieldDescriptor(
  name='repeated_import_enum_extension', full_name='protobuf_unittest.repeated_import_enum_extension', index=47,
  number=53, type=14, cpp_type=8, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
REPEATED_STRING_PIECE_EXTENSION_FIELD_NUMBER = 54
repeated_string_piece_extension = _descriptor.FieldDescriptor(
  name='repeated_string_piece_extension', full_name='protobuf_unittest.repeated_string_piece_extension', index=48,
  number=54, type=9, cpp_type=9, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002')))
REPEATED_CORD_EXTENSION_FIELD_NUMBER = 55
repeated_cord_extension = _descriptor.FieldDescriptor(
  name='repeated_cord_extension', full_name='protobuf_unittest.repeated_cord_extension', index=49,
  number=55, type=9, cpp_type=9, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001')))
REPEATED_LAZY_MESSAGE_EXTENSION_FIELD_NUMBER = 57
repeated_lazy_message_extension = _descriptor.FieldDescriptor(
  name='repeated_lazy_message_extension', full_name='protobuf_unittest.repeated_lazy_message_extension', index=50,
  number=57, type=11, cpp_type=10, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001')))
DEFAULT_INT32_EXTENSION_FIELD_NUMBER = 61
default_int32_extension = _descriptor.FieldDescriptor(
  name='default_int32_extension', full_name='protobuf_unittest.default_int32_extension', index=51,
  number=61, type=5, cpp_type=1, label=1,
  has_default_value=True, default_value=41,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_INT64_EXTENSION_FIELD_NUMBER = 62
default_int64_extension = _descriptor.FieldDescriptor(
  name='default_int64_extension', full_name='protobuf_unittest.default_int64_extension', index=52,
  number=62, type=3, cpp_type=2, label=1,
  has_default_value=True, default_value=42,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_UINT32_EXTENSION_FIELD_NUMBER = 63
default_uint32_extension = _descriptor.FieldDescriptor(
  name='default_uint32_extension', full_name='protobuf_unittest.default_uint32_extension', index=53,
  number=63, type=13, cpp_type=3, label=1,
  has_default_value=True, default_value=43,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_UINT64_EXTENSION_FIELD_NUMBER = 64
default_uint64_extension = _descriptor.FieldDescriptor(
  name='default_uint64_extension', full_name='protobuf_unittest.default_uint64_extension', index=54,
  number=64, type=4, cpp_type=4, label=1,
  has_default_value=True, default_value=44,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_SINT32_EXTENSION_FIELD_NUMBER = 65
default_sint32_extension = _descriptor.FieldDescriptor(
  name='default_sint32_extension', full_name='protobuf_unittest.default_sint32_extension', index=55,
  number=65, type=17, cpp_type=1, label=1,
  has_default_value=True, default_value=-45,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_SINT64_EXTENSION_FIELD_NUMBER = 66
default_sint64_extension = _descriptor.FieldDescriptor(
  name='default_sint64_extension', full_name='protobuf_unittest.default_sint64_extension', index=56,
  number=66, type=18, cpp_type=2, label=1,
  has_default_value=True, default_value=46,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_FIXED32_EXTENSION_FIELD_NUMBER = 67
default_fixed32_extension = _descriptor.FieldDescriptor(
  name='default_fixed32_extension', full_name='protobuf_unittest.default_fixed32_extension', index=57,
  number=67, type=7, cpp_type=3, label=1,
  has_default_value=True, default_value=47,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_FIXED64_EXTENSION_FIELD_NUMBER = 68
default_fixed64_extension = _descriptor.FieldDescriptor(
  name='default_fixed64_extension', full_name='protobuf_unittest.default_fixed64_extension', index=58,
  number=68, type=6, cpp_type=4, label=1,
  has_default_value=True, default_value=48,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_SFIXED32_EXTENSION_FIELD_NUMBER = 69
default_sfixed32_extension = _descriptor.FieldDescriptor(
  name='default_sfixed32_extension', full_name='protobuf_unittest.default_sfixed32_extension', index=59,
  number=69, type=15, cpp_type=1, label=1,
  has_default_value=True, default_value=49,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_SFIXED64_EXTENSION_FIELD_NUMBER = 70
default_sfixed64_extension = _descriptor.FieldDescriptor(
  name='default_sfixed64_extension', full_name='protobuf_unittest.default_sfixed64_extension', index=60,
  number=70, type=16, cpp_type=2, label=1,
  has_default_value=True, default_value=-50,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_FLOAT_EXTENSION_FIELD_NUMBER = 71
default_float_extension = _descriptor.FieldDescriptor(
  name='default_float_extension', full_name='protobuf_unittest.default_float_extension', index=61,
  number=71, type=2, cpp_type=6, label=1,
  has_default_value=True, default_value=51.5,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_DOUBLE_EXTENSION_FIELD_NUMBER = 72
default_double_extension = _descriptor.FieldDescriptor(
  name='default_double_extension', full_name='protobuf_unittest.default_double_extension', index=62,
  number=72, type=1, cpp_type=5, label=1,
  has_default_value=True, default_value=52000,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_BOOL_EXTENSION_FIELD_NUMBER = 73
default_bool_extension = _descriptor.FieldDescriptor(
  name='default_bool_extension', full_name='protobuf_unittest.default_bool_extension', index=63,
  number=73, type=8, cpp_type=7, label=1,
  has_default_value=True, default_value=True,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_STRING_EXTENSION_FIELD_NUMBER = 74
default_string_extension = _descriptor.FieldDescriptor(
  name='default_string_extension', full_name='protobuf_unittest.default_string_extension', index=64,
  number=74, type=9, cpp_type=9, label=1,
  has_default_value=True, default_value=_b("hello").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_BYTES_EXTENSION_FIELD_NUMBER = 75
default_bytes_extension = _descriptor.FieldDescriptor(
  name='default_bytes_extension', full_name='protobuf_unittest.default_bytes_extension', index=65,
  number=75, type=12, cpp_type=9, label=1,
  has_default_value=True, default_value=_b("world"),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_NESTED_ENUM_EXTENSION_FIELD_NUMBER = 81
default_nested_enum_extension = _descriptor.FieldDescriptor(
  name='default_nested_enum_extension', full_name='protobuf_unittest.default_nested_enum_extension', index=66,
  number=81, type=14, cpp_type=8, label=1,
  has_default_value=True, default_value=2,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_FOREIGN_ENUM_EXTENSION_FIELD_NUMBER = 82
default_foreign_enum_extension = _descriptor.FieldDescriptor(
  name='default_foreign_enum_extension', full_name='protobuf_unittest.default_foreign_enum_extension', index=67,
  number=82, type=14, cpp_type=8, label=1,
  has_default_value=True, default_value=5,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_IMPORT_ENUM_EXTENSION_FIELD_NUMBER = 83
default_import_enum_extension = _descriptor.FieldDescriptor(
  name='default_import_enum_extension', full_name='protobuf_unittest.default_import_enum_extension', index=68,
  number=83, type=14, cpp_type=8, label=1,
  has_default_value=True, default_value=8,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DEFAULT_STRING_PIECE_EXTENSION_FIELD_NUMBER = 84
default_string_piece_extension = _descriptor.FieldDescriptor(
  name='default_string_piece_extension', full_name='protobuf_unittest.default_string_piece_extension', index=69,
  number=84, type=9, cpp_type=9, label=1,
  has_default_value=True, default_value=_b("abc").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002')))
DEFAULT_CORD_EXTENSION_FIELD_NUMBER = 85
default_cord_extension = _descriptor.FieldDescriptor(
  name='default_cord_extension', full_name='protobuf_unittest.default_cord_extension', index=70,
  number=85, type=9, cpp_type=9, label=1,
  has_default_value=True, default_value=_b("123").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001')))
ONEOF_UINT32_EXTENSION_FIELD_NUMBER = 111
oneof_uint32_extension = _descriptor.FieldDescriptor(
  name='oneof_uint32_extension', full_name='protobuf_unittest.oneof_uint32_extension', index=71,
  number=111, type=13, cpp_type=3, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
ONEOF_NESTED_MESSAGE_EXTENSION_FIELD_NUMBER = 112
oneof_nested_message_extension = _descriptor.FieldDescriptor(
  name='oneof_nested_message_extension', full_name='protobuf_unittest.oneof_nested_message_extension', index=72,
  number=112, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
ONEOF_STRING_EXTENSION_FIELD_NUMBER = 113
oneof_string_extension = _descriptor.FieldDescriptor(
  name='oneof_string_extension', full_name='protobuf_unittest.oneof_string_extension', index=73,
  number=113, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=_b("").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
ONEOF_BYTES_EXTENSION_FIELD_NUMBER = 114
oneof_bytes_extension = _descriptor.FieldDescriptor(
  name='oneof_bytes_extension', full_name='protobuf_unittest.oneof_bytes_extension', index=74,
  number=114, type=12, cpp_type=9, label=1,
  has_default_value=False, default_value=_b(""),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
MY_EXTENSION_STRING_FIELD_NUMBER = 50
my_extension_string = _descriptor.FieldDescriptor(
  name='my_extension_string', full_name='protobuf_unittest.my_extension_string', index=75,
  number=50, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=_b("").decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
MY_EXTENSION_INT_FIELD_NUMBER = 5
my_extension_int = _descriptor.FieldDescriptor(
  name='my_extension_int', full_name='protobuf_unittest.my_extension_int', index=76,
  number=5, type=5, cpp_type=1, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
PACKED_INT32_EXTENSION_FIELD_NUMBER = 90
packed_int32_extension = _descriptor.FieldDescriptor(
  name='packed_int32_extension', full_name='protobuf_unittest.packed_int32_extension', index=77,
  number=90, type=5, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_INT64_EXTENSION_FIELD_NUMBER = 91
packed_int64_extension = _descriptor.FieldDescriptor(
  name='packed_int64_extension', full_name='protobuf_unittest.packed_int64_extension', index=78,
  number=91, type=3, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_UINT32_EXTENSION_FIELD_NUMBER = 92
packed_uint32_extension = _descriptor.FieldDescriptor(
  name='packed_uint32_extension', full_name='protobuf_unittest.packed_uint32_extension', index=79,
  number=92, type=13, cpp_type=3, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_UINT64_EXTENSION_FIELD_NUMBER = 93
packed_uint64_extension = _descriptor.FieldDescriptor(
  name='packed_uint64_extension', full_name='protobuf_unittest.packed_uint64_extension', index=80,
  number=93, type=4, cpp_type=4, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_SINT32_EXTENSION_FIELD_NUMBER = 94
packed_sint32_extension = _descriptor.FieldDescriptor(
  name='packed_sint32_extension', full_name='protobuf_unittest.packed_sint32_extension', index=81,
  number=94, type=17, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_SINT64_EXTENSION_FIELD_NUMBER = 95
packed_sint64_extension = _descriptor.FieldDescriptor(
  name='packed_sint64_extension', full_name='protobuf_unittest.packed_sint64_extension', index=82,
  number=95, type=18, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_FIXED32_EXTENSION_FIELD_NUMBER = 96
packed_fixed32_extension = _descriptor.FieldDescriptor(
  name='packed_fixed32_extension', full_name='protobuf_unittest.packed_fixed32_extension', index=83,
  number=96, type=7, cpp_type=3, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_FIXED64_EXTENSION_FIELD_NUMBER = 97
packed_fixed64_extension = _descriptor.FieldDescriptor(
  name='packed_fixed64_extension', full_name='protobuf_unittest.packed_fixed64_extension', index=84,
  number=97, type=6, cpp_type=4, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_SFIXED32_EXTENSION_FIELD_NUMBER = 98
packed_sfixed32_extension = _descriptor.FieldDescriptor(
  name='packed_sfixed32_extension', full_name='protobuf_unittest.packed_sfixed32_extension', index=85,
  number=98, type=15, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_SFIXED64_EXTENSION_FIELD_NUMBER = 99
packed_sfixed64_extension = _descriptor.FieldDescriptor(
  name='packed_sfixed64_extension', full_name='protobuf_unittest.packed_sfixed64_extension', index=86,
  number=99, type=16, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_FLOAT_EXTENSION_FIELD_NUMBER = 100
packed_float_extension = _descriptor.FieldDescriptor(
  name='packed_float_extension', full_name='protobuf_unittest.packed_float_extension', index=87,
  number=100, type=2, cpp_type=6, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_DOUBLE_EXTENSION_FIELD_NUMBER = 101
packed_double_extension = _descriptor.FieldDescriptor(
  name='packed_double_extension', full_name='protobuf_unittest.packed_double_extension', index=88,
  number=101, type=1, cpp_type=5, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_BOOL_EXTENSION_FIELD_NUMBER = 102
packed_bool_extension = _descriptor.FieldDescriptor(
  name='packed_bool_extension', full_name='protobuf_unittest.packed_bool_extension', index=89,
  number=102, type=8, cpp_type=7, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
PACKED_ENUM_EXTENSION_FIELD_NUMBER = 103
packed_enum_extension = _descriptor.FieldDescriptor(
  name='packed_enum_extension', full_name='protobuf_unittest.packed_enum_extension', index=90,
  number=103, type=14, cpp_type=8, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')))
UNPACKED_INT32_EXTENSION_FIELD_NUMBER = 90
unpacked_int32_extension = _descriptor.FieldDescriptor(
  name='unpacked_int32_extension', full_name='protobuf_unittest.unpacked_int32_extension', index=91,
  number=90, type=5, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_INT64_EXTENSION_FIELD_NUMBER = 91
unpacked_int64_extension = _descriptor.FieldDescriptor(
  name='unpacked_int64_extension', full_name='protobuf_unittest.unpacked_int64_extension', index=92,
  number=91, type=3, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_UINT32_EXTENSION_FIELD_NUMBER = 92
unpacked_uint32_extension = _descriptor.FieldDescriptor(
  name='unpacked_uint32_extension', full_name='protobuf_unittest.unpacked_uint32_extension', index=93,
  number=92, type=13, cpp_type=3, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_UINT64_EXTENSION_FIELD_NUMBER = 93
unpacked_uint64_extension = _descriptor.FieldDescriptor(
  name='unpacked_uint64_extension', full_name='protobuf_unittest.unpacked_uint64_extension', index=94,
  number=93, type=4, cpp_type=4, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_SINT32_EXTENSION_FIELD_NUMBER = 94
unpacked_sint32_extension = _descriptor.FieldDescriptor(
  name='unpacked_sint32_extension', full_name='protobuf_unittest.unpacked_sint32_extension', index=95,
  number=94, type=17, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_SINT64_EXTENSION_FIELD_NUMBER = 95
unpacked_sint64_extension = _descriptor.FieldDescriptor(
  name='unpacked_sint64_extension', full_name='protobuf_unittest.unpacked_sint64_extension', index=96,
  number=95, type=18, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_FIXED32_EXTENSION_FIELD_NUMBER = 96
unpacked_fixed32_extension = _descriptor.FieldDescriptor(
  name='unpacked_fixed32_extension', full_name='protobuf_unittest.unpacked_fixed32_extension', index=97,
  number=96, type=7, cpp_type=3, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_FIXED64_EXTENSION_FIELD_NUMBER = 97
unpacked_fixed64_extension = _descriptor.FieldDescriptor(
  name='unpacked_fixed64_extension', full_name='protobuf_unittest.unpacked_fixed64_extension', index=98,
  number=97, type=6, cpp_type=4, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_SFIXED32_EXTENSION_FIELD_NUMBER = 98
unpacked_sfixed32_extension = _descriptor.FieldDescriptor(
  name='unpacked_sfixed32_extension', full_name='protobuf_unittest.unpacked_sfixed32_extension', index=99,
  number=98, type=15, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_SFIXED64_EXTENSION_FIELD_NUMBER = 99
unpacked_sfixed64_extension = _descriptor.FieldDescriptor(
  name='unpacked_sfixed64_extension', full_name='protobuf_unittest.unpacked_sfixed64_extension', index=100,
  number=99, type=16, cpp_type=2, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_FLOAT_EXTENSION_FIELD_NUMBER = 100
unpacked_float_extension = _descriptor.FieldDescriptor(
  name='unpacked_float_extension', full_name='protobuf_unittest.unpacked_float_extension', index=101,
  number=100, type=2, cpp_type=6, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_DOUBLE_EXTENSION_FIELD_NUMBER = 101
unpacked_double_extension = _descriptor.FieldDescriptor(
  name='unpacked_double_extension', full_name='protobuf_unittest.unpacked_double_extension', index=102,
  number=101, type=1, cpp_type=5, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_BOOL_EXTENSION_FIELD_NUMBER = 102
unpacked_bool_extension = _descriptor.FieldDescriptor(
  name='unpacked_bool_extension', full_name='protobuf_unittest.unpacked_bool_extension', index=103,
  number=102, type=8, cpp_type=7, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))
UNPACKED_ENUM_EXTENSION_FIELD_NUMBER = 103
unpacked_enum_extension = _descriptor.FieldDescriptor(
  name='unpacked_enum_extension', full_name='protobuf_unittest.unpacked_enum_extension', index=104,
  number=103, type=14, cpp_type=8, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000')))

_TESTALLTYPES_NESTEDENUM = _descriptor.EnumDescriptor(
  name='NestedEnum',
  full_name='protobuf_unittest.TestAllTypes.NestedEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FOO', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAR', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAZ', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEG', index=3, number=-1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=3202,
  serialized_end=3259,
)
_sym_db.RegisterEnumDescriptor(_TESTALLTYPES_NESTEDENUM)

_TESTONEOF2_NESTEDENUM = _descriptor.EnumDescriptor(
  name='NestedEnum',
  full_name='protobuf_unittest.TestOneof2.NestedEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FOO', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAR', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAZ', index=2, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=3202,
  serialized_end=3241,
)
_sym_db.RegisterEnumDescriptor(_TESTONEOF2_NESTEDENUM)

_TESTDYNAMICEXTENSIONS_DYNAMICENUMTYPE = _descriptor.EnumDescriptor(
  name='DynamicEnumType',
  full_name='protobuf_unittest.TestDynamicExtensions.DynamicEnumType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DYNAMIC_FOO', index=0, number=2200,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DYNAMIC_BAR', index=1, number=2201,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DYNAMIC_BAZ', index=2, number=2202,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=10483,
  serialized_end=10554,
)
_sym_db.RegisterEnumDescriptor(_TESTDYNAMICEXTENSIONS_DYNAMICENUMTYPE)


_TESTALLTYPES_NESTEDMESSAGE = _descriptor.Descriptor(
  name='NestedMessage',
  full_name='protobuf_unittest.TestAllTypes.NestedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bb', full_name='protobuf_unittest.TestAllTypes.NestedMessage.bb', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3117,
  serialized_end=3144,
)

_TESTALLTYPES_OPTIONALGROUP = _descriptor.Descriptor(
  name='OptionalGroup',
  full_name='protobuf_unittest.TestAllTypes.OptionalGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestAllTypes.OptionalGroup.a', index=0,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3146,
  serialized_end=3172,
)

_TESTALLTYPES_REPEATEDGROUP = _descriptor.Descriptor(
  name='RepeatedGroup',
  full_name='protobuf_unittest.TestAllTypes.RepeatedGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestAllTypes.RepeatedGroup.a', index=0,
      number=47, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3174,
  serialized_end=3200,
)

_TESTALLTYPES = _descriptor.Descriptor(
  name='TestAllTypes',
  full_name='protobuf_unittest.TestAllTypes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optional_int32', full_name='protobuf_unittest.TestAllTypes.optional_int32', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_int64', full_name='protobuf_unittest.TestAllTypes.optional_int64', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_uint32', full_name='protobuf_unittest.TestAllTypes.optional_uint32', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_uint64', full_name='protobuf_unittest.TestAllTypes.optional_uint64', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_sint32', full_name='protobuf_unittest.TestAllTypes.optional_sint32', index=4,
      number=5, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_sint64', full_name='protobuf_unittest.TestAllTypes.optional_sint64', index=5,
      number=6, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_fixed32', full_name='protobuf_unittest.TestAllTypes.optional_fixed32', index=6,
      number=7, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_fixed64', full_name='protobuf_unittest.TestAllTypes.optional_fixed64', index=7,
      number=8, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_sfixed32', full_name='protobuf_unittest.TestAllTypes.optional_sfixed32', index=8,
      number=9, type=15, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_sfixed64', full_name='protobuf_unittest.TestAllTypes.optional_sfixed64', index=9,
      number=10, type=16, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_float', full_name='protobuf_unittest.TestAllTypes.optional_float', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_double', full_name='protobuf_unittest.TestAllTypes.optional_double', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_bool', full_name='protobuf_unittest.TestAllTypes.optional_bool', index=12,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_string', full_name='protobuf_unittest.TestAllTypes.optional_string', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_bytes', full_name='protobuf_unittest.TestAllTypes.optional_bytes', index=14,
      number=15, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optionalgroup', full_name='protobuf_unittest.TestAllTypes.optionalgroup', index=15,
      number=16, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_nested_message', full_name='protobuf_unittest.TestAllTypes.optional_nested_message', index=16,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_foreign_message', full_name='protobuf_unittest.TestAllTypes.optional_foreign_message', index=17,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_import_message', full_name='protobuf_unittest.TestAllTypes.optional_import_message', index=18,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_nested_enum', full_name='protobuf_unittest.TestAllTypes.optional_nested_enum', index=19,
      number=21, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_foreign_enum', full_name='protobuf_unittest.TestAllTypes.optional_foreign_enum', index=20,
      number=22, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=4,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_import_enum', full_name='protobuf_unittest.TestAllTypes.optional_import_enum', index=21,
      number=23, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=7,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_string_piece', full_name='protobuf_unittest.TestAllTypes.optional_string_piece', index=22,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='optional_cord', full_name='protobuf_unittest.TestAllTypes.optional_cord', index=23,
      number=25, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='optional_public_import_message', full_name='protobuf_unittest.TestAllTypes.optional_public_import_message', index=24,
      number=26, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_lazy_message', full_name='protobuf_unittest.TestAllTypes.optional_lazy_message', index=25,
      number=27, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))),
    _descriptor.FieldDescriptor(
      name='repeated_int32', full_name='protobuf_unittest.TestAllTypes.repeated_int32', index=26,
      number=31, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_int64', full_name='protobuf_unittest.TestAllTypes.repeated_int64', index=27,
      number=32, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_uint32', full_name='protobuf_unittest.TestAllTypes.repeated_uint32', index=28,
      number=33, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_uint64', full_name='protobuf_unittest.TestAllTypes.repeated_uint64', index=29,
      number=34, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_sint32', full_name='protobuf_unittest.TestAllTypes.repeated_sint32', index=30,
      number=35, type=17, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_sint64', full_name='protobuf_unittest.TestAllTypes.repeated_sint64', index=31,
      number=36, type=18, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_fixed32', full_name='protobuf_unittest.TestAllTypes.repeated_fixed32', index=32,
      number=37, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_fixed64', full_name='protobuf_unittest.TestAllTypes.repeated_fixed64', index=33,
      number=38, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_sfixed32', full_name='protobuf_unittest.TestAllTypes.repeated_sfixed32', index=34,
      number=39, type=15, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_sfixed64', full_name='protobuf_unittest.TestAllTypes.repeated_sfixed64', index=35,
      number=40, type=16, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_float', full_name='protobuf_unittest.TestAllTypes.repeated_float', index=36,
      number=41, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_double', full_name='protobuf_unittest.TestAllTypes.repeated_double', index=37,
      number=42, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_bool', full_name='protobuf_unittest.TestAllTypes.repeated_bool', index=38,
      number=43, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_string', full_name='protobuf_unittest.TestAllTypes.repeated_string', index=39,
      number=44, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_bytes', full_name='protobuf_unittest.TestAllTypes.repeated_bytes', index=40,
      number=45, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeatedgroup', full_name='protobuf_unittest.TestAllTypes.repeatedgroup', index=41,
      number=46, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_nested_message', full_name='protobuf_unittest.TestAllTypes.repeated_nested_message', index=42,
      number=48, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_foreign_message', full_name='protobuf_unittest.TestAllTypes.repeated_foreign_message', index=43,
      number=49, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_import_message', full_name='protobuf_unittest.TestAllTypes.repeated_import_message', index=44,
      number=50, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_nested_enum', full_name='protobuf_unittest.TestAllTypes.repeated_nested_enum', index=45,
      number=51, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_foreign_enum', full_name='protobuf_unittest.TestAllTypes.repeated_foreign_enum', index=46,
      number=52, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_import_enum', full_name='protobuf_unittest.TestAllTypes.repeated_import_enum', index=47,
      number=53, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_string_piece', full_name='protobuf_unittest.TestAllTypes.repeated_string_piece', index=48,
      number=54, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='repeated_cord', full_name='protobuf_unittest.TestAllTypes.repeated_cord', index=49,
      number=55, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='repeated_lazy_message', full_name='protobuf_unittest.TestAllTypes.repeated_lazy_message', index=50,
      number=57, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))),
    _descriptor.FieldDescriptor(
      name='default_int32', full_name='protobuf_unittest.TestAllTypes.default_int32', index=51,
      number=61, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=41,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_int64', full_name='protobuf_unittest.TestAllTypes.default_int64', index=52,
      number=62, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=42,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_uint32', full_name='protobuf_unittest.TestAllTypes.default_uint32', index=53,
      number=63, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=43,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_uint64', full_name='protobuf_unittest.TestAllTypes.default_uint64', index=54,
      number=64, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=44,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_sint32', full_name='protobuf_unittest.TestAllTypes.default_sint32', index=55,
      number=65, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=-45,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_sint64', full_name='protobuf_unittest.TestAllTypes.default_sint64', index=56,
      number=66, type=18, cpp_type=2, label=1,
      has_default_value=True, default_value=46,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_fixed32', full_name='protobuf_unittest.TestAllTypes.default_fixed32', index=57,
      number=67, type=7, cpp_type=3, label=1,
      has_default_value=True, default_value=47,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_fixed64', full_name='protobuf_unittest.TestAllTypes.default_fixed64', index=58,
      number=68, type=6, cpp_type=4, label=1,
      has_default_value=True, default_value=48,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_sfixed32', full_name='protobuf_unittest.TestAllTypes.default_sfixed32', index=59,
      number=69, type=15, cpp_type=1, label=1,
      has_default_value=True, default_value=49,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_sfixed64', full_name='protobuf_unittest.TestAllTypes.default_sfixed64', index=60,
      number=70, type=16, cpp_type=2, label=1,
      has_default_value=True, default_value=-50,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_float', full_name='protobuf_unittest.TestAllTypes.default_float', index=61,
      number=71, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=51.5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_double', full_name='protobuf_unittest.TestAllTypes.default_double', index=62,
      number=72, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=52000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_bool', full_name='protobuf_unittest.TestAllTypes.default_bool', index=63,
      number=73, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_string', full_name='protobuf_unittest.TestAllTypes.default_string', index=64,
      number=74, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("hello").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_bytes', full_name='protobuf_unittest.TestAllTypes.default_bytes', index=65,
      number=75, type=12, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("world"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_nested_enum', full_name='protobuf_unittest.TestAllTypes.default_nested_enum', index=66,
      number=81, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_foreign_enum', full_name='protobuf_unittest.TestAllTypes.default_foreign_enum', index=67,
      number=82, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_import_enum', full_name='protobuf_unittest.TestAllTypes.default_import_enum', index=68,
      number=83, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=8,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_string_piece', full_name='protobuf_unittest.TestAllTypes.default_string_piece', index=69,
      number=84, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("abc").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='default_cord', full_name='protobuf_unittest.TestAllTypes.default_cord', index=70,
      number=85, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("123").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='oneof_uint32', full_name='protobuf_unittest.TestAllTypes.oneof_uint32', index=71,
      number=111, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oneof_nested_message', full_name='protobuf_unittest.TestAllTypes.oneof_nested_message', index=72,
      number=112, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oneof_string', full_name='protobuf_unittest.TestAllTypes.oneof_string', index=73,
      number=113, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='oneof_bytes', full_name='protobuf_unittest.TestAllTypes.oneof_bytes', index=74,
      number=114, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTALLTYPES_NESTEDMESSAGE, _TESTALLTYPES_OPTIONALGROUP, _TESTALLTYPES_REPEATEDGROUP, ],
  enum_types=[
    _TESTALLTYPES_NESTEDENUM,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='oneof_field', full_name='protobuf_unittest.TestAllTypes.oneof_field',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=93,
  serialized_end=3274,
)


_NESTEDTESTALLTYPES = _descriptor.Descriptor(
  name='NestedTestAllTypes',
  full_name='protobuf_unittest.NestedTestAllTypes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='child', full_name='protobuf_unittest.NestedTestAllTypes.child', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payload', full_name='protobuf_unittest.NestedTestAllTypes.payload', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3276,
  serialized_end=3400,
)


_TESTDEPRECATEDFIELDS = _descriptor.Descriptor(
  name='TestDeprecatedFields',
  full_name='protobuf_unittest.TestDeprecatedFields',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deprecated_int32', full_name='protobuf_unittest.TestDeprecatedFields.deprecated_int32', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\030\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3402,
  serialized_end=3454,
)


_FOREIGNMESSAGE = _descriptor.Descriptor(
  name='ForeignMessage',
  full_name='protobuf_unittest.ForeignMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='c', full_name='protobuf_unittest.ForeignMessage.c', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3456,
  serialized_end=3483,
)


_TESTALLEXTENSIONS = _descriptor.Descriptor(
  name='TestAllExtensions',
  full_name='protobuf_unittest.TestAllExtensions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(1, 536870912), ],
  oneofs=[
  ],
  serialized_start=3485,
  serialized_end=3514,
)


_OPTIONALGROUP_EXTENSION = _descriptor.Descriptor(
  name='OptionalGroup_extension',
  full_name='protobuf_unittest.OptionalGroup_extension',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.OptionalGroup_extension.a', index=0,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3516,
  serialized_end=3552,
)


_REPEATEDGROUP_EXTENSION = _descriptor.Descriptor(
  name='RepeatedGroup_extension',
  full_name='protobuf_unittest.RepeatedGroup_extension',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.RepeatedGroup_extension.a', index=0,
      number=47, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3554,
  serialized_end=3590,
)


_TESTNESTEDEXTENSION = _descriptor.Descriptor(
  name='TestNestedExtension',
  full_name='protobuf_unittest.TestNestedExtension',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='test', full_name='protobuf_unittest.TestNestedExtension.test', index=0,
      number=1002, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("test").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nested_string_extension', full_name='protobuf_unittest.TestNestedExtension.nested_string_extension', index=1,
      number=1003, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3593,
  serialized_end=3745,
)


_TESTREQUIRED = _descriptor.Descriptor(
  name='TestRequired',
  full_name='protobuf_unittest.TestRequired',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestRequired.a', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy2', full_name='protobuf_unittest.TestRequired.dummy2', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='b', full_name='protobuf_unittest.TestRequired.b', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy4', full_name='protobuf_unittest.TestRequired.dummy4', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy5', full_name='protobuf_unittest.TestRequired.dummy5', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy6', full_name='protobuf_unittest.TestRequired.dummy6', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy7', full_name='protobuf_unittest.TestRequired.dummy7', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy8', full_name='protobuf_unittest.TestRequired.dummy8', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy9', full_name='protobuf_unittest.TestRequired.dummy9', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy10', full_name='protobuf_unittest.TestRequired.dummy10', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy11', full_name='protobuf_unittest.TestRequired.dummy11', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy12', full_name='protobuf_unittest.TestRequired.dummy12', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy13', full_name='protobuf_unittest.TestRequired.dummy13', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy14', full_name='protobuf_unittest.TestRequired.dummy14', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy15', full_name='protobuf_unittest.TestRequired.dummy15', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy16', full_name='protobuf_unittest.TestRequired.dummy16', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy17', full_name='protobuf_unittest.TestRequired.dummy17', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy18', full_name='protobuf_unittest.TestRequired.dummy18', index=17,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy19', full_name='protobuf_unittest.TestRequired.dummy19', index=18,
      number=19, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy20', full_name='protobuf_unittest.TestRequired.dummy20', index=19,
      number=20, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy21', full_name='protobuf_unittest.TestRequired.dummy21', index=20,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy22', full_name='protobuf_unittest.TestRequired.dummy22', index=21,
      number=22, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy23', full_name='protobuf_unittest.TestRequired.dummy23', index=22,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy24', full_name='protobuf_unittest.TestRequired.dummy24', index=23,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy25', full_name='protobuf_unittest.TestRequired.dummy25', index=24,
      number=25, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy26', full_name='protobuf_unittest.TestRequired.dummy26', index=25,
      number=26, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy27', full_name='protobuf_unittest.TestRequired.dummy27', index=26,
      number=27, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy28', full_name='protobuf_unittest.TestRequired.dummy28', index=27,
      number=28, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy29', full_name='protobuf_unittest.TestRequired.dummy29', index=28,
      number=29, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy30', full_name='protobuf_unittest.TestRequired.dummy30', index=29,
      number=30, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy31', full_name='protobuf_unittest.TestRequired.dummy31', index=30,
      number=31, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy32', full_name='protobuf_unittest.TestRequired.dummy32', index=31,
      number=32, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='c', full_name='protobuf_unittest.TestRequired.c', index=32,
      number=33, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='single', full_name='protobuf_unittest.TestRequired.single', index=0,
      number=1000, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='multi', full_name='protobuf_unittest.TestRequired.multi', index=1,
      number=1001, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3748,
  serialized_end=4473,
)


_TESTREQUIREDFOREIGN = _descriptor.Descriptor(
  name='TestRequiredForeign',
  full_name='protobuf_unittest.TestRequiredForeign',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optional_message', full_name='protobuf_unittest.TestRequiredForeign.optional_message', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_message', full_name='protobuf_unittest.TestRequiredForeign.repeated_message', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dummy', full_name='protobuf_unittest.TestRequiredForeign.dummy', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4476,
  serialized_end=4630,
)


_TESTFOREIGNNESTED = _descriptor.Descriptor(
  name='TestForeignNested',
  full_name='protobuf_unittest.TestForeignNested',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foreign_nested', full_name='protobuf_unittest.TestForeignNested.foreign_nested', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4632,
  serialized_end=4722,
)


_TESTEMPTYMESSAGE = _descriptor.Descriptor(
  name='TestEmptyMessage',
  full_name='protobuf_unittest.TestEmptyMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4724,
  serialized_end=4742,
)


_TESTEMPTYMESSAGEWITHEXTENSIONS = _descriptor.Descriptor(
  name='TestEmptyMessageWithExtensions',
  full_name='protobuf_unittest.TestEmptyMessageWithExtensions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(1, 536870912), ],
  oneofs=[
  ],
  serialized_start=4744,
  serialized_end=4786,
)


_TESTMULTIPLEEXTENSIONRANGES = _descriptor.Descriptor(
  name='TestMultipleExtensionRanges',
  full_name='protobuf_unittest.TestMultipleExtensionRanges',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(42, 43), (4143, 4244), (65536, 536870912), ],
  oneofs=[
  ],
  serialized_start=4788,
  serialized_end=4843,
)


_TESTREALLYLARGETAGNUMBER = _descriptor.Descriptor(
  name='TestReallyLargeTagNumber',
  full_name='protobuf_unittest.TestReallyLargeTagNumber',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestReallyLargeTagNumber.a', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bb', full_name='protobuf_unittest.TestReallyLargeTagNumber.bb', index=1,
      number=268435455, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4845,
  serialized_end=4897,
)


_TESTRECURSIVEMESSAGE = _descriptor.Descriptor(
  name='TestRecursiveMessage',
  full_name='protobuf_unittest.TestRecursiveMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestRecursiveMessage.a', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i', full_name='protobuf_unittest.TestRecursiveMessage.i', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4899,
  serialized_end=4984,
)


_TESTMUTUALRECURSIONA = _descriptor.Descriptor(
  name='TestMutualRecursionA',
  full_name='protobuf_unittest.TestMutualRecursionA',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bb', full_name='protobuf_unittest.TestMutualRecursionA.bb', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4986,
  serialized_end=5061,
)


_TESTMUTUALRECURSIONB = _descriptor.Descriptor(
  name='TestMutualRecursionB',
  full_name='protobuf_unittest.TestMutualRecursionB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestMutualRecursionB.a', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_int32', full_name='protobuf_unittest.TestMutualRecursionB.optional_int32', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5063,
  serialized_end=5161,
)


_TESTDUPFIELDNUMBER_FOO = _descriptor.Descriptor(
  name='Foo',
  full_name='protobuf_unittest.TestDupFieldNumber.Foo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestDupFieldNumber.Foo.a', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5309,
  serialized_end=5325,
)

_TESTDUPFIELDNUMBER_BAR = _descriptor.Descriptor(
  name='Bar',
  full_name='protobuf_unittest.TestDupFieldNumber.Bar',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestDupFieldNumber.Bar.a', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5327,
  serialized_end=5343,
)

_TESTDUPFIELDNUMBER = _descriptor.Descriptor(
  name='TestDupFieldNumber',
  full_name='protobuf_unittest.TestDupFieldNumber',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestDupFieldNumber.a', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo', full_name='protobuf_unittest.TestDupFieldNumber.foo', index=1,
      number=2, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bar', full_name='protobuf_unittest.TestDupFieldNumber.bar', index=2,
      number=3, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTDUPFIELDNUMBER_FOO, _TESTDUPFIELDNUMBER_BAR, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5164,
  serialized_end=5343,
)


_TESTEAGERMESSAGE = _descriptor.Descriptor(
  name='TestEagerMessage',
  full_name='protobuf_unittest.TestEagerMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sub_message', full_name='protobuf_unittest.TestEagerMessage.sub_message', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\000'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5345,
  serialized_end=5421,
)


_TESTLAZYMESSAGE = _descriptor.Descriptor(
  name='TestLazyMessage',
  full_name='protobuf_unittest.TestLazyMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sub_message', full_name='protobuf_unittest.TestLazyMessage.sub_message', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5423,
  serialized_end=5498,
)


_TESTNESTEDMESSAGEHASBITS_NESTEDMESSAGE = _descriptor.Descriptor(
  name='NestedMessage',
  full_name='protobuf_unittest.TestNestedMessageHasBits.NestedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nestedmessage_repeated_int32', full_name='protobuf_unittest.TestNestedMessageHasBits.NestedMessage.nestedmessage_repeated_int32', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nestedmessage_repeated_foreignmessage', full_name='protobuf_unittest.TestNestedMessageHasBits.NestedMessage.nestedmessage_repeated_foreignmessage', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5622,
  serialized_end=5757,
)

_TESTNESTEDMESSAGEHASBITS = _descriptor.Descriptor(
  name='TestNestedMessageHasBits',
  full_name='protobuf_unittest.TestNestedMessageHasBits',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optional_nested_message', full_name='protobuf_unittest.TestNestedMessageHasBits.optional_nested_message', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTNESTEDMESSAGEHASBITS_NESTEDMESSAGE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5501,
  serialized_end=5757,
)


_TESTCAMELCASEFIELDNAMES = _descriptor.Descriptor(
  name='TestCamelCaseFieldNames',
  full_name='protobuf_unittest.TestCamelCaseFieldNames',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='PrimitiveField', full_name='protobuf_unittest.TestCamelCaseFieldNames.PrimitiveField', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='StringField', full_name='protobuf_unittest.TestCamelCaseFieldNames.StringField', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='EnumField', full_name='protobuf_unittest.TestCamelCaseFieldNames.EnumField', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=4,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='MessageField', full_name='protobuf_unittest.TestCamelCaseFieldNames.MessageField', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='StringPieceField', full_name='protobuf_unittest.TestCamelCaseFieldNames.StringPieceField', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='CordField', full_name='protobuf_unittest.TestCamelCaseFieldNames.CordField', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='RepeatedPrimitiveField', full_name='protobuf_unittest.TestCamelCaseFieldNames.RepeatedPrimitiveField', index=6,
      number=7, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='RepeatedStringField', full_name='protobuf_unittest.TestCamelCaseFieldNames.RepeatedStringField', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='RepeatedEnumField', full_name='protobuf_unittest.TestCamelCaseFieldNames.RepeatedEnumField', index=8,
      number=9, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='RepeatedMessageField', full_name='protobuf_unittest.TestCamelCaseFieldNames.RepeatedMessageField', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='RepeatedStringPieceField', full_name='protobuf_unittest.TestCamelCaseFieldNames.RepeatedStringPieceField', index=10,
      number=11, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='RepeatedCordField', full_name='protobuf_unittest.TestCamelCaseFieldNames.RepeatedCordField', index=11,
      number=12, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5760,
  serialized_end=6245,
)


_TESTFIELDORDERINGS = _descriptor.Descriptor(
  name='TestFieldOrderings',
  full_name='protobuf_unittest.TestFieldOrderings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='my_string', full_name='protobuf_unittest.TestFieldOrderings.my_string', index=0,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='my_int', full_name='protobuf_unittest.TestFieldOrderings.my_int', index=1,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='my_float', full_name='protobuf_unittest.TestFieldOrderings.my_float', index=2,
      number=101, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(2, 11), (12, 101), ],
  oneofs=[
  ],
  serialized_start=6247,
  serialized_end=6332,
)


_TESTEXTREMEDEFAULTVALUES = _descriptor.Descriptor(
  name='TestExtremeDefaultValues',
  full_name='protobuf_unittest.TestExtremeDefaultValues',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='escaped_bytes', full_name='protobuf_unittest.TestExtremeDefaultValues.escaped_bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("\000\001\007\010\014\n\r\t\013\\\'\"\376"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='large_uint32', full_name='protobuf_unittest.TestExtremeDefaultValues.large_uint32', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=4294967295,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='large_uint64', full_name='protobuf_unittest.TestExtremeDefaultValues.large_uint64', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=18446744073709551615,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='small_int32', full_name='protobuf_unittest.TestExtremeDefaultValues.small_int32', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-2147483647,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='small_int64', full_name='protobuf_unittest.TestExtremeDefaultValues.small_int64', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=-9223372036854775807,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='really_small_int32', full_name='protobuf_unittest.TestExtremeDefaultValues.really_small_int32', index=5,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-2147483648,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='really_small_int64', full_name='protobuf_unittest.TestExtremeDefaultValues.really_small_int64', index=6,
      number=22, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=-9223372036854775808,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='utf8_string', full_name='protobuf_unittest.TestExtremeDefaultValues.utf8_string', index=7,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("\341\210\264").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zero_float', full_name='protobuf_unittest.TestExtremeDefaultValues.zero_float', index=8,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='one_float', full_name='protobuf_unittest.TestExtremeDefaultValues.one_float', index=9,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='small_float', full_name='protobuf_unittest.TestExtremeDefaultValues.small_float', index=10,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=1.5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='negative_one_float', full_name='protobuf_unittest.TestExtremeDefaultValues.negative_one_float', index=11,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='negative_float', full_name='protobuf_unittest.TestExtremeDefaultValues.negative_float', index=12,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=-1.5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='large_float', full_name='protobuf_unittest.TestExtremeDefaultValues.large_float', index=13,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=2e+008,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='small_negative_float', full_name='protobuf_unittest.TestExtremeDefaultValues.small_negative_float', index=14,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=-8e-028,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inf_double', full_name='protobuf_unittest.TestExtremeDefaultValues.inf_double', index=15,
      number=14, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='neg_inf_double', full_name='protobuf_unittest.TestExtremeDefaultValues.neg_inf_double', index=16,
      number=15, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=-1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nan_double', full_name='protobuf_unittest.TestExtremeDefaultValues.nan_double', index=17,
      number=16, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=(1e10000 * 0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inf_float', full_name='protobuf_unittest.TestExtremeDefaultValues.inf_float', index=18,
      number=17, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='neg_inf_float', full_name='protobuf_unittest.TestExtremeDefaultValues.neg_inf_float', index=19,
      number=18, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=-1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nan_float', full_name='protobuf_unittest.TestExtremeDefaultValues.nan_float', index=20,
      number=19, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=(1e10000 * 0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cpp_trigraph', full_name='protobuf_unittest.TestExtremeDefaultValues.cpp_trigraph', index=21,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("? ? ?? ?? ??? ??/ ??-").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='string_with_zero', full_name='protobuf_unittest.TestExtremeDefaultValues.string_with_zero', index=22,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("hel\000lo").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bytes_with_zero', full_name='protobuf_unittest.TestExtremeDefaultValues.bytes_with_zero', index=23,
      number=24, type=12, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("wor\000ld"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='string_piece_with_zero', full_name='protobuf_unittest.TestExtremeDefaultValues.string_piece_with_zero', index=24,
      number=25, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("ab\000c").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='cord_with_zero', full_name='protobuf_unittest.TestExtremeDefaultValues.cord_with_zero', index=25,
      number=26, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("12\0003").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='replacement_string', full_name='protobuf_unittest.TestExtremeDefaultValues.replacement_string', index=26,
      number=27, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("${unknown}").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6335,
  serialized_end=7287,
)


_SPARSEENUMMESSAGE = _descriptor.Descriptor(
  name='SparseEnumMessage',
  full_name='protobuf_unittest.SparseEnumMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sparse_enum', full_name='protobuf_unittest.SparseEnumMessage.sparse_enum', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=123,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7289,
  serialized_end=7364,
)


_ONESTRING = _descriptor.Descriptor(
  name='OneString',
  full_name='protobuf_unittest.OneString',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.OneString.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7366,
  serialized_end=7391,
)


_MORESTRING = _descriptor.Descriptor(
  name='MoreString',
  full_name='protobuf_unittest.MoreString',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.MoreString.data', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7393,
  serialized_end=7419,
)


_ONEBYTES = _descriptor.Descriptor(
  name='OneBytes',
  full_name='protobuf_unittest.OneBytes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.OneBytes.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7421,
  serialized_end=7445,
)


_MOREBYTES = _descriptor.Descriptor(
  name='MoreBytes',
  full_name='protobuf_unittest.MoreBytes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.MoreBytes.data', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7447,
  serialized_end=7472,
)


_INT32MESSAGE = _descriptor.Descriptor(
  name='Int32Message',
  full_name='protobuf_unittest.Int32Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.Int32Message.data', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7474,
  serialized_end=7502,
)


_UINT32MESSAGE = _descriptor.Descriptor(
  name='Uint32Message',
  full_name='protobuf_unittest.Uint32Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.Uint32Message.data', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7504,
  serialized_end=7533,
)


_INT64MESSAGE = _descriptor.Descriptor(
  name='Int64Message',
  full_name='protobuf_unittest.Int64Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.Int64Message.data', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7535,
  serialized_end=7563,
)


_UINT64MESSAGE = _descriptor.Descriptor(
  name='Uint64Message',
  full_name='protobuf_unittest.Uint64Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.Uint64Message.data', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7565,
  serialized_end=7594,
)


_BOOLMESSAGE = _descriptor.Descriptor(
  name='BoolMessage',
  full_name='protobuf_unittest.BoolMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='protobuf_unittest.BoolMessage.data', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7596,
  serialized_end=7623,
)


_TESTONEOF_FOOGROUP = _descriptor.Descriptor(
  name='FooGroup',
  full_name='protobuf_unittest.TestOneof.FooGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestOneof.FooGroup.a', index=0,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='b', full_name='protobuf_unittest.TestOneof.FooGroup.b', index=1,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7795,
  serialized_end=7827,
)

_TESTONEOF = _descriptor.Descriptor(
  name='TestOneof',
  full_name='protobuf_unittest.TestOneof',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo_int', full_name='protobuf_unittest.TestOneof.foo_int', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_string', full_name='protobuf_unittest.TestOneof.foo_string', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_message', full_name='protobuf_unittest.TestOneof.foo_message', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foogroup', full_name='protobuf_unittest.TestOneof.foogroup', index=3,
      number=4, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTONEOF_FOOGROUP, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='foo', full_name='protobuf_unittest.TestOneof.foo',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=7626,
  serialized_end=7834,
)


_TESTONEOFBACKWARDSCOMPATIBLE_FOOGROUP = _descriptor.Descriptor(
  name='FooGroup',
  full_name='protobuf_unittest.TestOneofBackwardsCompatible.FooGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestOneofBackwardsCompatible.FooGroup.a', index=0,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='b', full_name='protobuf_unittest.TestOneofBackwardsCompatible.FooGroup.b', index=1,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7795,
  serialized_end=7827,
)

_TESTONEOFBACKWARDSCOMPATIBLE = _descriptor.Descriptor(
  name='TestOneofBackwardsCompatible',
  full_name='protobuf_unittest.TestOneofBackwardsCompatible',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo_int', full_name='protobuf_unittest.TestOneofBackwardsCompatible.foo_int', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_string', full_name='protobuf_unittest.TestOneofBackwardsCompatible.foo_string', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_message', full_name='protobuf_unittest.TestOneofBackwardsCompatible.foo_message', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foogroup', full_name='protobuf_unittest.TestOneofBackwardsCompatible.foogroup', index=3,
      number=4, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTONEOFBACKWARDSCOMPATIBLE_FOOGROUP, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7837,
  serialized_end=8068,
)


_TESTONEOF2_FOOGROUP = _descriptor.Descriptor(
  name='FooGroup',
  full_name='protobuf_unittest.TestOneof2.FooGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestOneof2.FooGroup.a', index=0,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='b', full_name='protobuf_unittest.TestOneof2.FooGroup.b', index=1,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=8729,
  serialized_end=8761,
)

_TESTONEOF2_NESTEDMESSAGE = _descriptor.Descriptor(
  name='NestedMessage',
  full_name='protobuf_unittest.TestOneof2.NestedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='qux_int', full_name='protobuf_unittest.TestOneof2.NestedMessage.qux_int', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='corge_int', full_name='protobuf_unittest.TestOneof2.NestedMessage.corge_int', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=8763,
  serialized_end=8814,
)

_TESTONEOF2 = _descriptor.Descriptor(
  name='TestOneof2',
  full_name='protobuf_unittest.TestOneof2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo_int', full_name='protobuf_unittest.TestOneof2.foo_int', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_string', full_name='protobuf_unittest.TestOneof2.foo_string', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_cord', full_name='protobuf_unittest.TestOneof2.foo_cord', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='foo_string_piece', full_name='protobuf_unittest.TestOneof2.foo_string_piece', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='foo_bytes', full_name='protobuf_unittest.TestOneof2.foo_bytes', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_enum', full_name='protobuf_unittest.TestOneof2.foo_enum', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_message', full_name='protobuf_unittest.TestOneof2.foo_message', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foogroup', full_name='protobuf_unittest.TestOneof2.foogroup', index=7,
      number=8, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_lazy_message', full_name='protobuf_unittest.TestOneof2.foo_lazy_message', index=8,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))),
    _descriptor.FieldDescriptor(
      name='bar_int', full_name='protobuf_unittest.TestOneof2.bar_int', index=9,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bar_string', full_name='protobuf_unittest.TestOneof2.bar_string', index=10,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("STRING").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bar_cord', full_name='protobuf_unittest.TestOneof2.bar_cord', index=11,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("CORD").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))),
    _descriptor.FieldDescriptor(
      name='bar_string_piece', full_name='protobuf_unittest.TestOneof2.bar_string_piece', index=12,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("SPIECE").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))),
    _descriptor.FieldDescriptor(
      name='bar_bytes', full_name='protobuf_unittest.TestOneof2.bar_bytes', index=13,
      number=16, type=12, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("BYTES"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bar_enum', full_name='protobuf_unittest.TestOneof2.bar_enum', index=14,
      number=17, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baz_int', full_name='protobuf_unittest.TestOneof2.baz_int', index=15,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baz_string', full_name='protobuf_unittest.TestOneof2.baz_string', index=16,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("BAZ").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTONEOF2_FOOGROUP, _TESTONEOF2_NESTEDMESSAGE, ],
  enum_types=[
    _TESTONEOF2_NESTEDENUM,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='foo', full_name='protobuf_unittest.TestOneof2.foo',
      index=0, containing_type=None, fields=[]),
    _descriptor.OneofDescriptor(
      name='bar', full_name='protobuf_unittest.TestOneof2.bar',
      index=1, containing_type=None, fields=[]),
  ],
  serialized_start=8071,
  serialized_end=8869,
)


_TESTREQUIREDONEOF_NESTEDMESSAGE = _descriptor.Descriptor(
  name='NestedMessage',
  full_name='protobuf_unittest.TestRequiredOneof.NestedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='required_double', full_name='protobuf_unittest.TestRequiredOneof.NestedMessage.required_double', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=9009,
  serialized_end=9049,
)

_TESTREQUIREDONEOF = _descriptor.Descriptor(
  name='TestRequiredOneof',
  full_name='protobuf_unittest.TestRequiredOneof',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo_int', full_name='protobuf_unittest.TestRequiredOneof.foo_int', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_string', full_name='protobuf_unittest.TestRequiredOneof.foo_string', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foo_message', full_name='protobuf_unittest.TestRequiredOneof.foo_message', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTREQUIREDONEOF_NESTEDMESSAGE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='foo', full_name='protobuf_unittest.TestRequiredOneof.foo',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=8872,
  serialized_end=9056,
)


_TESTPACKEDTYPES = _descriptor.Descriptor(
  name='TestPackedTypes',
  full_name='protobuf_unittest.TestPackedTypes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packed_int32', full_name='protobuf_unittest.TestPackedTypes.packed_int32', index=0,
      number=90, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_int64', full_name='protobuf_unittest.TestPackedTypes.packed_int64', index=1,
      number=91, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_uint32', full_name='protobuf_unittest.TestPackedTypes.packed_uint32', index=2,
      number=92, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_uint64', full_name='protobuf_unittest.TestPackedTypes.packed_uint64', index=3,
      number=93, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_sint32', full_name='protobuf_unittest.TestPackedTypes.packed_sint32', index=4,
      number=94, type=17, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_sint64', full_name='protobuf_unittest.TestPackedTypes.packed_sint64', index=5,
      number=95, type=18, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_fixed32', full_name='protobuf_unittest.TestPackedTypes.packed_fixed32', index=6,
      number=96, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_fixed64', full_name='protobuf_unittest.TestPackedTypes.packed_fixed64', index=7,
      number=97, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_sfixed32', full_name='protobuf_unittest.TestPackedTypes.packed_sfixed32', index=8,
      number=98, type=15, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_sfixed64', full_name='protobuf_unittest.TestPackedTypes.packed_sfixed64', index=9,
      number=99, type=16, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_float', full_name='protobuf_unittest.TestPackedTypes.packed_float', index=10,
      number=100, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_double', full_name='protobuf_unittest.TestPackedTypes.packed_double', index=11,
      number=101, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_bool', full_name='protobuf_unittest.TestPackedTypes.packed_bool', index=12,
      number=102, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='packed_enum', full_name='protobuf_unittest.TestPackedTypes.packed_enum', index=13,
      number=103, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=9059,
  serialized_end=9485,
)


_TESTUNPACKEDTYPES = _descriptor.Descriptor(
  name='TestUnpackedTypes',
  full_name='protobuf_unittest.TestUnpackedTypes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='unpacked_int32', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_int32', index=0,
      number=90, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_int64', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_int64', index=1,
      number=91, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_uint32', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_uint32', index=2,
      number=92, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_uint64', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_uint64', index=3,
      number=93, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_sint32', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_sint32', index=4,
      number=94, type=17, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_sint64', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_sint64', index=5,
      number=95, type=18, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_fixed32', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_fixed32', index=6,
      number=96, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_fixed64', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_fixed64', index=7,
      number=97, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_sfixed32', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_sfixed32', index=8,
      number=98, type=15, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_sfixed64', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_sfixed64', index=9,
      number=99, type=16, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_float', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_float', index=10,
      number=100, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_double', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_double', index=11,
      number=101, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_bool', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_bool', index=12,
      number=102, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
    _descriptor.FieldDescriptor(
      name='unpacked_enum', full_name='protobuf_unittest.TestUnpackedTypes.unpacked_enum', index=13,
      number=103, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=9488,
  serialized_end=9944,
)


_TESTPACKEDEXTENSIONS = _descriptor.Descriptor(
  name='TestPackedExtensions',
  full_name='protobuf_unittest.TestPackedExtensions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(1, 536870912), ],
  oneofs=[
  ],
  serialized_start=9946,
  serialized_end=9978,
)


_TESTUNPACKEDEXTENSIONS = _descriptor.Descriptor(
  name='TestUnpackedExtensions',
  full_name='protobuf_unittest.TestUnpackedExtensions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(1, 536870912), ],
  oneofs=[
  ],
  serialized_start=9980,
  serialized_end=10014,
)


_TESTDYNAMICEXTENSIONS_DYNAMICMESSAGETYPE = _descriptor.Descriptor(
  name='DynamicMessageType',
  full_name='protobuf_unittest.TestDynamicExtensions.DynamicMessageType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dynamic_field', full_name='protobuf_unittest.TestDynamicExtensions.DynamicMessageType.dynamic_field', index=0,
      number=2100, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=10437,
  serialized_end=10481,
)

_TESTDYNAMICEXTENSIONS = _descriptor.Descriptor(
  name='TestDynamicExtensions',
  full_name='protobuf_unittest.TestDynamicExtensions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='scalar_extension', full_name='protobuf_unittest.TestDynamicExtensions.scalar_extension', index=0,
      number=2000, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enum_extension', full_name='protobuf_unittest.TestDynamicExtensions.enum_extension', index=1,
      number=2001, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=4,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dynamic_enum_extension', full_name='protobuf_unittest.TestDynamicExtensions.dynamic_enum_extension', index=2,
      number=2002, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=2200,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message_extension', full_name='protobuf_unittest.TestDynamicExtensions.message_extension', index=3,
      number=2003, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dynamic_message_extension', full_name='protobuf_unittest.TestDynamicExtensions.dynamic_message_extension', index=4,
      number=2004, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_extension', full_name='protobuf_unittest.TestDynamicExtensions.repeated_extension', index=5,
      number=2005, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='packed_extension', full_name='protobuf_unittest.TestDynamicExtensions.packed_extension', index=6,
      number=2006, type=17, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[_TESTDYNAMICEXTENSIONS_DYNAMICMESSAGETYPE, ],
  enum_types=[
    _TESTDYNAMICEXTENSIONS_DYNAMICENUMTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=10017,
  serialized_end=10554,
)


_TESTREPEATEDSCALARDIFFERENTTAGSIZES = _descriptor.Descriptor(
  name='TestRepeatedScalarDifferentTagSizes',
  full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='repeated_fixed32', full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes.repeated_fixed32', index=0,
      number=12, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_int32', full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes.repeated_int32', index=1,
      number=13, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_fixed64', full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes.repeated_fixed64', index=2,
      number=2046, type=6, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_int64', full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes.repeated_int64', index=3,
      number=2047, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_float', full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes.repeated_float', index=4,
      number=262142, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_uint64', full_name='protobuf_unittest.TestRepeatedScalarDifferentTagSizes.repeated_uint64', index=5,
      number=262143, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=10557,
  serialized_end=10749,
)


_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP1 = _descriptor.Descriptor(
  name='Group1',
  full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.Group1',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field1', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.Group1.field1', index=0,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=11542,
  serialized_end=11599,
)

_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP2 = _descriptor.Descriptor(
  name='Group2',
  full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.Group2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field1', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.Group2.field1', index=0,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=11601,
  serialized_end=11658,
)

_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR = _descriptor.Descriptor(
  name='RepeatedFieldsGenerator',
  full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field1', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.field1', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='field2', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.field2', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='field3', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.field3', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='group1', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.group1', index=3,
      number=10, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='group2', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.group2', index=4,
      number=20, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext1', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.ext1', index=5,
      number=1000, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext2', full_name='protobuf_unittest.TestParsingMerge.RepeatedFieldsGenerator.ext2', index=6,
      number=1001, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP1, _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP2, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=11104,
  serialized_end=11658,
)

_TESTPARSINGMERGE_OPTIONALGROUP = _descriptor.Descriptor(
  name='OptionalGroup',
  full_name='protobuf_unittest.TestParsingMerge.OptionalGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optional_group_all_types', full_name='protobuf_unittest.TestParsingMerge.OptionalGroup.optional_group_all_types', index=0,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=11660,
  serialized_end=11742,
)

_TESTPARSINGMERGE_REPEATEDGROUP = _descriptor.Descriptor(
  name='RepeatedGroup',
  full_name='protobuf_unittest.TestParsingMerge.RepeatedGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='repeated_group_all_types', full_name='protobuf_unittest.TestParsingMerge.RepeatedGroup.repeated_group_all_types', index=0,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=11744,
  serialized_end=11826,
)

_TESTPARSINGMERGE = _descriptor.Descriptor(
  name='TestParsingMerge',
  full_name='protobuf_unittest.TestParsingMerge',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='required_all_types', full_name='protobuf_unittest.TestParsingMerge.required_all_types', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optional_all_types', full_name='protobuf_unittest.TestParsingMerge.optional_all_types', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_all_types', full_name='protobuf_unittest.TestParsingMerge.repeated_all_types', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optionalgroup', full_name='protobuf_unittest.TestParsingMerge.optionalgroup', index=3,
      number=10, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeatedgroup', full_name='protobuf_unittest.TestParsingMerge.repeatedgroup', index=4,
      number=20, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='optional_ext', full_name='protobuf_unittest.TestParsingMerge.optional_ext', index=0,
      number=1000, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repeated_ext', full_name='protobuf_unittest.TestParsingMerge.repeated_ext', index=1,
      number=1001, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR, _TESTPARSINGMERGE_OPTIONALGROUP, _TESTPARSINGMERGE_REPEATEDGROUP, ],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  extension_ranges=[(1000, 536870912), ],
  oneofs=[
  ],
  serialized_start=10752,
  serialized_end=12023,
)


_TESTCOMMENTINJECTIONMESSAGE = _descriptor.Descriptor(
  name='TestCommentInjectionMessage',
  full_name='protobuf_unittest.TestCommentInjectionMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='protobuf_unittest.TestCommentInjectionMessage.a', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("*/ <- Neither should this.").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12025,
  serialized_end=12093,
)


_FOOREQUEST = _descriptor.Descriptor(
  name='FooRequest',
  full_name='protobuf_unittest.FooRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12095,
  serialized_end=12107,
)


_FOORESPONSE = _descriptor.Descriptor(
  name='FooResponse',
  full_name='protobuf_unittest.FooResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12109,
  serialized_end=12122,
)


_FOOCLIENTMESSAGE = _descriptor.Descriptor(
  name='FooClientMessage',
  full_name='protobuf_unittest.FooClientMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12124,
  serialized_end=12142,
)


_FOOSERVERMESSAGE = _descriptor.Descriptor(
  name='FooServerMessage',
  full_name='protobuf_unittest.FooServerMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12144,
  serialized_end=12162,
)


_BARREQUEST = _descriptor.Descriptor(
  name='BarRequest',
  full_name='protobuf_unittest.BarRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12164,
  serialized_end=12176,
)


_BARRESPONSE = _descriptor.Descriptor(
  name='BarResponse',
  full_name='protobuf_unittest.BarResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12178,
  serialized_end=12191,
)

_TESTALLTYPES_NESTEDMESSAGE.containing_type = _TESTALLTYPES
_TESTALLTYPES_OPTIONALGROUP.containing_type = _TESTALLTYPES
_TESTALLTYPES_REPEATEDGROUP.containing_type = _TESTALLTYPES
_TESTALLTYPES.fields_by_name['optionalgroup'].message_type = _TESTALLTYPES_OPTIONALGROUP
_TESTALLTYPES.fields_by_name['optional_nested_message'].message_type = _TESTALLTYPES_NESTEDMESSAGE
_TESTALLTYPES.fields_by_name['optional_foreign_message'].message_type = _FOREIGNMESSAGE
_TESTALLTYPES.fields_by_name['optional_import_message'].message_type = google.protobuf.unittest_import_pb2._IMPORTMESSAGE
_TESTALLTYPES.fields_by_name['optional_nested_enum'].enum_type = _TESTALLTYPES_NESTEDENUM
_TESTALLTYPES.fields_by_name['optional_foreign_enum'].enum_type = _FOREIGNENUM
_TESTALLTYPES.fields_by_name['optional_import_enum'].enum_type = google.protobuf.unittest_import_pb2._IMPORTENUM
_TESTALLTYPES.fields_by_name['optional_public_import_message'].message_type = google.protobuf.unittest_import_public_pb2._PUBLICIMPORTMESSAGE
_TESTALLTYPES.fields_by_name['optional_lazy_message'].message_type = _TESTALLTYPES_NESTEDMESSAGE
_TESTALLTYPES.fields_by_name['repeatedgroup'].message_type = _TESTALLTYPES_REPEATEDGROUP
_TESTALLTYPES.fields_by_name['repeated_nested_message'].message_type = _TESTALLTYPES_NESTEDMESSAGE
_TESTALLTYPES.fields_by_name['repeated_foreign_message'].message_type = _FOREIGNMESSAGE
_TESTALLTYPES.fields_by_name['repeated_import_message'].message_type = google.protobuf.unittest_import_pb2._IMPORTMESSAGE
_TESTALLTYPES.fields_by_name['repeated_nested_enum'].enum_type = _TESTALLTYPES_NESTEDENUM
_TESTALLTYPES.fields_by_name['repeated_foreign_enum'].enum_type = _FOREIGNENUM
_TESTALLTYPES.fields_by_name['repeated_import_enum'].enum_type = google.protobuf.unittest_import_pb2._IMPORTENUM
_TESTALLTYPES.fields_by_name['repeated_lazy_message'].message_type = _TESTALLTYPES_NESTEDMESSAGE
_TESTALLTYPES.fields_by_name['default_nested_enum'].enum_type = _TESTALLTYPES_NESTEDENUM
_TESTALLTYPES.fields_by_name['default_foreign_enum'].enum_type = _FOREIGNENUM
_TESTALLTYPES.fields_by_name['default_import_enum'].enum_type = google.protobuf.unittest_import_pb2._IMPORTENUM
_TESTALLTYPES.fields_by_name['oneof_nested_message'].message_type = _TESTALLTYPES_NESTEDMESSAGE
_TESTALLTYPES_NESTEDENUM.containing_type = _TESTALLTYPES
_TESTALLTYPES.oneofs_by_name['oneof_field'].fields.append(
  _TESTALLTYPES.fields_by_name['oneof_uint32'])
_TESTALLTYPES.fields_by_name['oneof_uint32'].containing_oneof = _TESTALLTYPES.oneofs_by_name['oneof_field']
_TESTALLTYPES.oneofs_by_name['oneof_field'].fields.append(
  _TESTALLTYPES.fields_by_name['oneof_nested_message'])
_TESTALLTYPES.fields_by_name['oneof_nested_message'].containing_oneof = _TESTALLTYPES.oneofs_by_name['oneof_field']
_TESTALLTYPES.oneofs_by_name['oneof_field'].fields.append(
  _TESTALLTYPES.fields_by_name['oneof_string'])
_TESTALLTYPES.fields_by_name['oneof_string'].containing_oneof = _TESTALLTYPES.oneofs_by_name['oneof_field']
_TESTALLTYPES.oneofs_by_name['oneof_field'].fields.append(
  _TESTALLTYPES.fields_by_name['oneof_bytes'])
_TESTALLTYPES.fields_by_name['oneof_bytes'].containing_oneof = _TESTALLTYPES.oneofs_by_name['oneof_field']
_NESTEDTESTALLTYPES.fields_by_name['child'].message_type = _NESTEDTESTALLTYPES
_NESTEDTESTALLTYPES.fields_by_name['payload'].message_type = _TESTALLTYPES
_TESTREQUIREDFOREIGN.fields_by_name['optional_message'].message_type = _TESTREQUIRED
_TESTREQUIREDFOREIGN.fields_by_name['repeated_message'].message_type = _TESTREQUIRED
_TESTFOREIGNNESTED.fields_by_name['foreign_nested'].message_type = _TESTALLTYPES_NESTEDMESSAGE
_TESTRECURSIVEMESSAGE.fields_by_name['a'].message_type = _TESTRECURSIVEMESSAGE
_TESTMUTUALRECURSIONA.fields_by_name['bb'].message_type = _TESTMUTUALRECURSIONB
_TESTMUTUALRECURSIONB.fields_by_name['a'].message_type = _TESTMUTUALRECURSIONA
_TESTDUPFIELDNUMBER_FOO.containing_type = _TESTDUPFIELDNUMBER
_TESTDUPFIELDNUMBER_BAR.containing_type = _TESTDUPFIELDNUMBER
_TESTDUPFIELDNUMBER.fields_by_name['foo'].message_type = _TESTDUPFIELDNUMBER_FOO
_TESTDUPFIELDNUMBER.fields_by_name['bar'].message_type = _TESTDUPFIELDNUMBER_BAR
_TESTEAGERMESSAGE.fields_by_name['sub_message'].message_type = _TESTALLTYPES
_TESTLAZYMESSAGE.fields_by_name['sub_message'].message_type = _TESTALLTYPES
_TESTNESTEDMESSAGEHASBITS_NESTEDMESSAGE.fields_by_name['nestedmessage_repeated_foreignmessage'].message_type = _FOREIGNMESSAGE
_TESTNESTEDMESSAGEHASBITS_NESTEDMESSAGE.containing_type = _TESTNESTEDMESSAGEHASBITS
_TESTNESTEDMESSAGEHASBITS.fields_by_name['optional_nested_message'].message_type = _TESTNESTEDMESSAGEHASBITS_NESTEDMESSAGE
_TESTCAMELCASEFIELDNAMES.fields_by_name['EnumField'].enum_type = _FOREIGNENUM
_TESTCAMELCASEFIELDNAMES.fields_by_name['MessageField'].message_type = _FOREIGNMESSAGE
_TESTCAMELCASEFIELDNAMES.fields_by_name['RepeatedEnumField'].enum_type = _FOREIGNENUM
_TESTCAMELCASEFIELDNAMES.fields_by_name['RepeatedMessageField'].message_type = _FOREIGNMESSAGE
_SPARSEENUMMESSAGE.fields_by_name['sparse_enum'].enum_type = _TESTSPARSEENUM
_TESTONEOF_FOOGROUP.containing_type = _TESTONEOF
_TESTONEOF.fields_by_name['foo_message'].message_type = _TESTALLTYPES
_TESTONEOF.fields_by_name['foogroup'].message_type = _TESTONEOF_FOOGROUP
_TESTONEOF.oneofs_by_name['foo'].fields.append(
  _TESTONEOF.fields_by_name['foo_int'])
_TESTONEOF.fields_by_name['foo_int'].containing_oneof = _TESTONEOF.oneofs_by_name['foo']
_TESTONEOF.oneofs_by_name['foo'].fields.append(
  _TESTONEOF.fields_by_name['foo_string'])
_TESTONEOF.fields_by_name['foo_string'].containing_oneof = _TESTONEOF.oneofs_by_name['foo']
_TESTONEOF.oneofs_by_name['foo'].fields.append(
  _TESTONEOF.fields_by_name['foo_message'])
_TESTONEOF.fields_by_name['foo_message'].containing_oneof = _TESTONEOF.oneofs_by_name['foo']
_TESTONEOF.oneofs_by_name['foo'].fields.append(
  _TESTONEOF.fields_by_name['foogroup'])
_TESTONEOF.fields_by_name['foogroup'].containing_oneof = _TESTONEOF.oneofs_by_name['foo']
_TESTONEOFBACKWARDSCOMPATIBLE_FOOGROUP.containing_type = _TESTONEOFBACKWARDSCOMPATIBLE
_TESTONEOFBACKWARDSCOMPATIBLE.fields_by_name['foo_message'].message_type = _TESTALLTYPES
_TESTONEOFBACKWARDSCOMPATIBLE.fields_by_name['foogroup'].message_type = _TESTONEOFBACKWARDSCOMPATIBLE_FOOGROUP
_TESTONEOF2_FOOGROUP.containing_type = _TESTONEOF2
_TESTONEOF2_NESTEDMESSAGE.containing_type = _TESTONEOF2
_TESTONEOF2.fields_by_name['foo_enum'].enum_type = _TESTONEOF2_NESTEDENUM
_TESTONEOF2.fields_by_name['foo_message'].message_type = _TESTONEOF2_NESTEDMESSAGE
_TESTONEOF2.fields_by_name['foogroup'].message_type = _TESTONEOF2_FOOGROUP
_TESTONEOF2.fields_by_name['foo_lazy_message'].message_type = _TESTONEOF2_NESTEDMESSAGE
_TESTONEOF2.fields_by_name['bar_enum'].enum_type = _TESTONEOF2_NESTEDENUM
_TESTONEOF2_NESTEDENUM.containing_type = _TESTONEOF2
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_int'])
_TESTONEOF2.fields_by_name['foo_int'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_string'])
_TESTONEOF2.fields_by_name['foo_string'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_cord'])
_TESTONEOF2.fields_by_name['foo_cord'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_string_piece'])
_TESTONEOF2.fields_by_name['foo_string_piece'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_bytes'])
_TESTONEOF2.fields_by_name['foo_bytes'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_enum'])
_TESTONEOF2.fields_by_name['foo_enum'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_message'])
_TESTONEOF2.fields_by_name['foo_message'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foogroup'])
_TESTONEOF2.fields_by_name['foogroup'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['foo'].fields.append(
  _TESTONEOF2.fields_by_name['foo_lazy_message'])
_TESTONEOF2.fields_by_name['foo_lazy_message'].containing_oneof = _TESTONEOF2.oneofs_by_name['foo']
_TESTONEOF2.oneofs_by_name['bar'].fields.append(
  _TESTONEOF2.fields_by_name['bar_int'])
_TESTONEOF2.fields_by_name['bar_int'].containing_oneof = _TESTONEOF2.oneofs_by_name['bar']
_TESTONEOF2.oneofs_by_name['bar'].fields.append(
  _TESTONEOF2.fields_by_name['bar_string'])
_TESTONEOF2.fields_by_name['bar_string'].containing_oneof = _TESTONEOF2.oneofs_by_name['bar']
_TESTONEOF2.oneofs_by_name['bar'].fields.append(
  _TESTONEOF2.fields_by_name['bar_cord'])
_TESTONEOF2.fields_by_name['bar_cord'].containing_oneof = _TESTONEOF2.oneofs_by_name['bar']
_TESTONEOF2.oneofs_by_name['bar'].fields.append(
  _TESTONEOF2.fields_by_name['bar_string_piece'])
_TESTONEOF2.fields_by_name['bar_string_piece'].containing_oneof = _TESTONEOF2.oneofs_by_name['bar']
_TESTONEOF2.oneofs_by_name['bar'].fields.append(
  _TESTONEOF2.fields_by_name['bar_bytes'])
_TESTONEOF2.fields_by_name['bar_bytes'].containing_oneof = _TESTONEOF2.oneofs_by_name['bar']
_TESTONEOF2.oneofs_by_name['bar'].fields.append(
  _TESTONEOF2.fields_by_name['bar_enum'])
_TESTONEOF2.fields_by_name['bar_enum'].containing_oneof = _TESTONEOF2.oneofs_by_name['bar']
_TESTREQUIREDONEOF_NESTEDMESSAGE.containing_type = _TESTREQUIREDONEOF
_TESTREQUIREDONEOF.fields_by_name['foo_message'].message_type = _TESTREQUIREDONEOF_NESTEDMESSAGE
_TESTREQUIREDONEOF.oneofs_by_name['foo'].fields.append(
  _TESTREQUIREDONEOF.fields_by_name['foo_int'])
_TESTREQUIREDONEOF.fields_by_name['foo_int'].containing_oneof = _TESTREQUIREDONEOF.oneofs_by_name['foo']
_TESTREQUIREDONEOF.oneofs_by_name['foo'].fields.append(
  _TESTREQUIREDONEOF.fields_by_name['foo_string'])
_TESTREQUIREDONEOF.fields_by_name['foo_string'].containing_oneof = _TESTREQUIREDONEOF.oneofs_by_name['foo']
_TESTREQUIREDONEOF.oneofs_by_name['foo'].fields.append(
  _TESTREQUIREDONEOF.fields_by_name['foo_message'])
_TESTREQUIREDONEOF.fields_by_name['foo_message'].containing_oneof = _TESTREQUIREDONEOF.oneofs_by_name['foo']
_TESTPACKEDTYPES.fields_by_name['packed_enum'].enum_type = _FOREIGNENUM
_TESTUNPACKEDTYPES.fields_by_name['unpacked_enum'].enum_type = _FOREIGNENUM
_TESTDYNAMICEXTENSIONS_DYNAMICMESSAGETYPE.containing_type = _TESTDYNAMICEXTENSIONS
_TESTDYNAMICEXTENSIONS.fields_by_name['enum_extension'].enum_type = _FOREIGNENUM
_TESTDYNAMICEXTENSIONS.fields_by_name['dynamic_enum_extension'].enum_type = _TESTDYNAMICEXTENSIONS_DYNAMICENUMTYPE
_TESTDYNAMICEXTENSIONS.fields_by_name['message_extension'].message_type = _FOREIGNMESSAGE
_TESTDYNAMICEXTENSIONS.fields_by_name['dynamic_message_extension'].message_type = _TESTDYNAMICEXTENSIONS_DYNAMICMESSAGETYPE
_TESTDYNAMICEXTENSIONS_DYNAMICENUMTYPE.containing_type = _TESTDYNAMICEXTENSIONS
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP1.fields_by_name['field1'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP1.containing_type = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP2.fields_by_name['field1'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP2.containing_type = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['field1'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['field2'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['field3'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['group1'].message_type = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP1
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['group2'].message_type = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP2
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['ext1'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.fields_by_name['ext2'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR.containing_type = _TESTPARSINGMERGE
_TESTPARSINGMERGE_OPTIONALGROUP.fields_by_name['optional_group_all_types'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_OPTIONALGROUP.containing_type = _TESTPARSINGMERGE
_TESTPARSINGMERGE_REPEATEDGROUP.fields_by_name['repeated_group_all_types'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE_REPEATEDGROUP.containing_type = _TESTPARSINGMERGE
_TESTPARSINGMERGE.fields_by_name['required_all_types'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE.fields_by_name['optional_all_types'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE.fields_by_name['repeated_all_types'].message_type = _TESTALLTYPES
_TESTPARSINGMERGE.fields_by_name['optionalgroup'].message_type = _TESTPARSINGMERGE_OPTIONALGROUP
_TESTPARSINGMERGE.fields_by_name['repeatedgroup'].message_type = _TESTPARSINGMERGE_REPEATEDGROUP
DESCRIPTOR.message_types_by_name['TestAllTypes'] = _TESTALLTYPES
DESCRIPTOR.message_types_by_name['NestedTestAllTypes'] = _NESTEDTESTALLTYPES
DESCRIPTOR.message_types_by_name['TestDeprecatedFields'] = _TESTDEPRECATEDFIELDS
DESCRIPTOR.message_types_by_name['ForeignMessage'] = _FOREIGNMESSAGE
DESCRIPTOR.message_types_by_name['TestAllExtensions'] = _TESTALLEXTENSIONS
DESCRIPTOR.message_types_by_name['OptionalGroup_extension'] = _OPTIONALGROUP_EXTENSION
DESCRIPTOR.message_types_by_name['RepeatedGroup_extension'] = _REPEATEDGROUP_EXTENSION
DESCRIPTOR.message_types_by_name['TestNestedExtension'] = _TESTNESTEDEXTENSION
DESCRIPTOR.message_types_by_name['TestRequired'] = _TESTREQUIRED
DESCRIPTOR.message_types_by_name['TestRequiredForeign'] = _TESTREQUIREDFOREIGN
DESCRIPTOR.message_types_by_name['TestForeignNested'] = _TESTFOREIGNNESTED
DESCRIPTOR.message_types_by_name['TestEmptyMessage'] = _TESTEMPTYMESSAGE
DESCRIPTOR.message_types_by_name['TestEmptyMessageWithExtensions'] = _TESTEMPTYMESSAGEWITHEXTENSIONS
DESCRIPTOR.message_types_by_name['TestMultipleExtensionRanges'] = _TESTMULTIPLEEXTENSIONRANGES
DESCRIPTOR.message_types_by_name['TestReallyLargeTagNumber'] = _TESTREALLYLARGETAGNUMBER
DESCRIPTOR.message_types_by_name['TestRecursiveMessage'] = _TESTRECURSIVEMESSAGE
DESCRIPTOR.message_types_by_name['TestMutualRecursionA'] = _TESTMUTUALRECURSIONA
DESCRIPTOR.message_types_by_name['TestMutualRecursionB'] = _TESTMUTUALRECURSIONB
DESCRIPTOR.message_types_by_name['TestDupFieldNumber'] = _TESTDUPFIELDNUMBER
DESCRIPTOR.message_types_by_name['TestEagerMessage'] = _TESTEAGERMESSAGE
DESCRIPTOR.message_types_by_name['TestLazyMessage'] = _TESTLAZYMESSAGE
DESCRIPTOR.message_types_by_name['TestNestedMessageHasBits'] = _TESTNESTEDMESSAGEHASBITS
DESCRIPTOR.message_types_by_name['TestCamelCaseFieldNames'] = _TESTCAMELCASEFIELDNAMES
DESCRIPTOR.message_types_by_name['TestFieldOrderings'] = _TESTFIELDORDERINGS
DESCRIPTOR.message_types_by_name['TestExtremeDefaultValues'] = _TESTEXTREMEDEFAULTVALUES
DESCRIPTOR.message_types_by_name['SparseEnumMessage'] = _SPARSEENUMMESSAGE
DESCRIPTOR.message_types_by_name['OneString'] = _ONESTRING
DESCRIPTOR.message_types_by_name['MoreString'] = _MORESTRING
DESCRIPTOR.message_types_by_name['OneBytes'] = _ONEBYTES
DESCRIPTOR.message_types_by_name['MoreBytes'] = _MOREBYTES
DESCRIPTOR.message_types_by_name['Int32Message'] = _INT32MESSAGE
DESCRIPTOR.message_types_by_name['Uint32Message'] = _UINT32MESSAGE
DESCRIPTOR.message_types_by_name['Int64Message'] = _INT64MESSAGE
DESCRIPTOR.message_types_by_name['Uint64Message'] = _UINT64MESSAGE
DESCRIPTOR.message_types_by_name['BoolMessage'] = _BOOLMESSAGE
DESCRIPTOR.message_types_by_name['TestOneof'] = _TESTONEOF
DESCRIPTOR.message_types_by_name['TestOneofBackwardsCompatible'] = _TESTONEOFBACKWARDSCOMPATIBLE
DESCRIPTOR.message_types_by_name['TestOneof2'] = _TESTONEOF2
DESCRIPTOR.message_types_by_name['TestRequiredOneof'] = _TESTREQUIREDONEOF
DESCRIPTOR.message_types_by_name['TestPackedTypes'] = _TESTPACKEDTYPES
DESCRIPTOR.message_types_by_name['TestUnpackedTypes'] = _TESTUNPACKEDTYPES
DESCRIPTOR.message_types_by_name['TestPackedExtensions'] = _TESTPACKEDEXTENSIONS
DESCRIPTOR.message_types_by_name['TestUnpackedExtensions'] = _TESTUNPACKEDEXTENSIONS
DESCRIPTOR.message_types_by_name['TestDynamicExtensions'] = _TESTDYNAMICEXTENSIONS
DESCRIPTOR.message_types_by_name['TestRepeatedScalarDifferentTagSizes'] = _TESTREPEATEDSCALARDIFFERENTTAGSIZES
DESCRIPTOR.message_types_by_name['TestParsingMerge'] = _TESTPARSINGMERGE
DESCRIPTOR.message_types_by_name['TestCommentInjectionMessage'] = _TESTCOMMENTINJECTIONMESSAGE
DESCRIPTOR.message_types_by_name['FooRequest'] = _FOOREQUEST
DESCRIPTOR.message_types_by_name['FooResponse'] = _FOORESPONSE
DESCRIPTOR.message_types_by_name['FooClientMessage'] = _FOOCLIENTMESSAGE
DESCRIPTOR.message_types_by_name['FooServerMessage'] = _FOOSERVERMESSAGE
DESCRIPTOR.message_types_by_name['BarRequest'] = _BARREQUEST
DESCRIPTOR.message_types_by_name['BarResponse'] = _BARRESPONSE
DESCRIPTOR.enum_types_by_name['ForeignEnum'] = _FOREIGNENUM
DESCRIPTOR.enum_types_by_name['TestEnumWithDupValue'] = _TESTENUMWITHDUPVALUE
DESCRIPTOR.enum_types_by_name['TestSparseEnum'] = _TESTSPARSEENUM
DESCRIPTOR.extensions_by_name['optional_int32_extension'] = optional_int32_extension
DESCRIPTOR.extensions_by_name['optional_int64_extension'] = optional_int64_extension
DESCRIPTOR.extensions_by_name['optional_uint32_extension'] = optional_uint32_extension
DESCRIPTOR.extensions_by_name['optional_uint64_extension'] = optional_uint64_extension
DESCRIPTOR.extensions_by_name['optional_sint32_extension'] = optional_sint32_extension
DESCRIPTOR.extensions_by_name['optional_sint64_extension'] = optional_sint64_extension
DESCRIPTOR.extensions_by_name['optional_fixed32_extension'] = optional_fixed32_extension
DESCRIPTOR.extensions_by_name['optional_fixed64_extension'] = optional_fixed64_extension
DESCRIPTOR.extensions_by_name['optional_sfixed32_extension'] = optional_sfixed32_extension
DESCRIPTOR.extensions_by_name['optional_sfixed64_extension'] = optional_sfixed64_extension
DESCRIPTOR.extensions_by_name['optional_float_extension'] = optional_float_extension
DESCRIPTOR.extensions_by_name['optional_double_extension'] = optional_double_extension
DESCRIPTOR.extensions_by_name['optional_bool_extension'] = optional_bool_extension
DESCRIPTOR.extensions_by_name['optional_string_extension'] = optional_string_extension
DESCRIPTOR.extensions_by_name['optional_bytes_extension'] = optional_bytes_extension
DESCRIPTOR.extensions_by_name['optionalgroup_extension'] = optionalgroup_extension
DESCRIPTOR.extensions_by_name['optional_nested_message_extension'] = optional_nested_message_extension
DESCRIPTOR.extensions_by_name['optional_foreign_message_extension'] = optional_foreign_message_extension
DESCRIPTOR.extensions_by_name['optional_import_message_extension'] = optional_import_message_extension
DESCRIPTOR.extensions_by_name['optional_nested_enum_extension'] = optional_nested_enum_extension
DESCRIPTOR.extensions_by_name['optional_foreign_enum_extension'] = optional_foreign_enum_extension
DESCRIPTOR.extensions_by_name['optional_import_enum_extension'] = optional_import_enum_extension
DESCRIPTOR.extensions_by_name['optional_string_piece_extension'] = optional_string_piece_extension
DESCRIPTOR.extensions_by_name['optional_cord_extension'] = optional_cord_extension
DESCRIPTOR.extensions_by_name['optional_public_import_message_extension'] = optional_public_import_message_extension
DESCRIPTOR.extensions_by_name['optional_lazy_message_extension'] = optional_lazy_message_extension
DESCRIPTOR.extensions_by_name['repeated_int32_extension'] = repeated_int32_extension
DESCRIPTOR.extensions_by_name['repeated_int64_extension'] = repeated_int64_extension
DESCRIPTOR.extensions_by_name['repeated_uint32_extension'] = repeated_uint32_extension
DESCRIPTOR.extensions_by_name['repeated_uint64_extension'] = repeated_uint64_extension
DESCRIPTOR.extensions_by_name['repeated_sint32_extension'] = repeated_sint32_extension
DESCRIPTOR.extensions_by_name['repeated_sint64_extension'] = repeated_sint64_extension
DESCRIPTOR.extensions_by_name['repeated_fixed32_extension'] = repeated_fixed32_extension
DESCRIPTOR.extensions_by_name['repeated_fixed64_extension'] = repeated_fixed64_extension
DESCRIPTOR.extensions_by_name['repeated_sfixed32_extension'] = repeated_sfixed32_extension
DESCRIPTOR.extensions_by_name['repeated_sfixed64_extension'] = repeated_sfixed64_extension
DESCRIPTOR.extensions_by_name['repeated_float_extension'] = repeated_float_extension
DESCRIPTOR.extensions_by_name['repeated_double_extension'] = repeated_double_extension
DESCRIPTOR.extensions_by_name['repeated_bool_extension'] = repeated_bool_extension
DESCRIPTOR.extensions_by_name['repeated_string_extension'] = repeated_string_extension
DESCRIPTOR.extensions_by_name['repeated_bytes_extension'] = repeated_bytes_extension
DESCRIPTOR.extensions_by_name['repeatedgroup_extension'] = repeatedgroup_extension
DESCRIPTOR.extensions_by_name['repeated_nested_message_extension'] = repeated_nested_message_extension
DESCRIPTOR.extensions_by_name['repeated_foreign_message_extension'] = repeated_foreign_message_extension
DESCRIPTOR.extensions_by_name['repeated_import_message_extension'] = repeated_import_message_extension
DESCRIPTOR.extensions_by_name['repeated_nested_enum_extension'] = repeated_nested_enum_extension
DESCRIPTOR.extensions_by_name['repeated_foreign_enum_extension'] = repeated_foreign_enum_extension
DESCRIPTOR.extensions_by_name['repeated_import_enum_extension'] = repeated_import_enum_extension
DESCRIPTOR.extensions_by_name['repeated_string_piece_extension'] = repeated_string_piece_extension
DESCRIPTOR.extensions_by_name['repeated_cord_extension'] = repeated_cord_extension
DESCRIPTOR.extensions_by_name['repeated_lazy_message_extension'] = repeated_lazy_message_extension
DESCRIPTOR.extensions_by_name['default_int32_extension'] = default_int32_extension
DESCRIPTOR.extensions_by_name['default_int64_extension'] = default_int64_extension
DESCRIPTOR.extensions_by_name['default_uint32_extension'] = default_uint32_extension
DESCRIPTOR.extensions_by_name['default_uint64_extension'] = default_uint64_extension
DESCRIPTOR.extensions_by_name['default_sint32_extension'] = default_sint32_extension
DESCRIPTOR.extensions_by_name['default_sint64_extension'] = default_sint64_extension
DESCRIPTOR.extensions_by_name['default_fixed32_extension'] = default_fixed32_extension
DESCRIPTOR.extensions_by_name['default_fixed64_extension'] = default_fixed64_extension
DESCRIPTOR.extensions_by_name['default_sfixed32_extension'] = default_sfixed32_extension
DESCRIPTOR.extensions_by_name['default_sfixed64_extension'] = default_sfixed64_extension
DESCRIPTOR.extensions_by_name['default_float_extension'] = default_float_extension
DESCRIPTOR.extensions_by_name['default_double_extension'] = default_double_extension
DESCRIPTOR.extensions_by_name['default_bool_extension'] = default_bool_extension
DESCRIPTOR.extensions_by_name['default_string_extension'] = default_string_extension
DESCRIPTOR.extensions_by_name['default_bytes_extension'] = default_bytes_extension
DESCRIPTOR.extensions_by_name['default_nested_enum_extension'] = default_nested_enum_extension
DESCRIPTOR.extensions_by_name['default_foreign_enum_extension'] = default_foreign_enum_extension
DESCRIPTOR.extensions_by_name['default_import_enum_extension'] = default_import_enum_extension
DESCRIPTOR.extensions_by_name['default_string_piece_extension'] = default_string_piece_extension
DESCRIPTOR.extensions_by_name['default_cord_extension'] = default_cord_extension
DESCRIPTOR.extensions_by_name['oneof_uint32_extension'] = oneof_uint32_extension
DESCRIPTOR.extensions_by_name['oneof_nested_message_extension'] = oneof_nested_message_extension
DESCRIPTOR.extensions_by_name['oneof_string_extension'] = oneof_string_extension
DESCRIPTOR.extensions_by_name['oneof_bytes_extension'] = oneof_bytes_extension
DESCRIPTOR.extensions_by_name['my_extension_string'] = my_extension_string
DESCRIPTOR.extensions_by_name['my_extension_int'] = my_extension_int
DESCRIPTOR.extensions_by_name['packed_int32_extension'] = packed_int32_extension
DESCRIPTOR.extensions_by_name['packed_int64_extension'] = packed_int64_extension
DESCRIPTOR.extensions_by_name['packed_uint32_extension'] = packed_uint32_extension
DESCRIPTOR.extensions_by_name['packed_uint64_extension'] = packed_uint64_extension
DESCRIPTOR.extensions_by_name['packed_sint32_extension'] = packed_sint32_extension
DESCRIPTOR.extensions_by_name['packed_sint64_extension'] = packed_sint64_extension
DESCRIPTOR.extensions_by_name['packed_fixed32_extension'] = packed_fixed32_extension
DESCRIPTOR.extensions_by_name['packed_fixed64_extension'] = packed_fixed64_extension
DESCRIPTOR.extensions_by_name['packed_sfixed32_extension'] = packed_sfixed32_extension
DESCRIPTOR.extensions_by_name['packed_sfixed64_extension'] = packed_sfixed64_extension
DESCRIPTOR.extensions_by_name['packed_float_extension'] = packed_float_extension
DESCRIPTOR.extensions_by_name['packed_double_extension'] = packed_double_extension
DESCRIPTOR.extensions_by_name['packed_bool_extension'] = packed_bool_extension
DESCRIPTOR.extensions_by_name['packed_enum_extension'] = packed_enum_extension
DESCRIPTOR.extensions_by_name['unpacked_int32_extension'] = unpacked_int32_extension
DESCRIPTOR.extensions_by_name['unpacked_int64_extension'] = unpacked_int64_extension
DESCRIPTOR.extensions_by_name['unpacked_uint32_extension'] = unpacked_uint32_extension
DESCRIPTOR.extensions_by_name['unpacked_uint64_extension'] = unpacked_uint64_extension
DESCRIPTOR.extensions_by_name['unpacked_sint32_extension'] = unpacked_sint32_extension
DESCRIPTOR.extensions_by_name['unpacked_sint64_extension'] = unpacked_sint64_extension
DESCRIPTOR.extensions_by_name['unpacked_fixed32_extension'] = unpacked_fixed32_extension
DESCRIPTOR.extensions_by_name['unpacked_fixed64_extension'] = unpacked_fixed64_extension
DESCRIPTOR.extensions_by_name['unpacked_sfixed32_extension'] = unpacked_sfixed32_extension
DESCRIPTOR.extensions_by_name['unpacked_sfixed64_extension'] = unpacked_sfixed64_extension
DESCRIPTOR.extensions_by_name['unpacked_float_extension'] = unpacked_float_extension
DESCRIPTOR.extensions_by_name['unpacked_double_extension'] = unpacked_double_extension
DESCRIPTOR.extensions_by_name['unpacked_bool_extension'] = unpacked_bool_extension
DESCRIPTOR.extensions_by_name['unpacked_enum_extension'] = unpacked_enum_extension

TestAllTypes = _reflection.GeneratedProtocolMessageType('TestAllTypes', (_message.Message,), dict(

  NestedMessage = _reflection.GeneratedProtocolMessageType('NestedMessage', (_message.Message,), dict(
    DESCRIPTOR = _TESTALLTYPES_NESTEDMESSAGE,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,

  OptionalGroup = _reflection.GeneratedProtocolMessageType('OptionalGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTALLTYPES_OPTIONALGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,

  RepeatedGroup = _reflection.GeneratedProtocolMessageType('RepeatedGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTALLTYPES_REPEATEDGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTALLTYPES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestAllTypes)
_sym_db.RegisterMessage(TestAllTypes.NestedMessage)
_sym_db.RegisterMessage(TestAllTypes.OptionalGroup)
_sym_db.RegisterMessage(TestAllTypes.RepeatedGroup)

NestedTestAllTypes = _reflection.GeneratedProtocolMessageType('NestedTestAllTypes', (_message.Message,), dict(
  DESCRIPTOR = _NESTEDTESTALLTYPES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(NestedTestAllTypes)

TestDeprecatedFields = _reflection.GeneratedProtocolMessageType('TestDeprecatedFields', (_message.Message,), dict(
  DESCRIPTOR = _TESTDEPRECATEDFIELDS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestDeprecatedFields)

ForeignMessage = _reflection.GeneratedProtocolMessageType('ForeignMessage', (_message.Message,), dict(
  DESCRIPTOR = _FOREIGNMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(ForeignMessage)

TestAllExtensions = _reflection.GeneratedProtocolMessageType('TestAllExtensions', (_message.Message,), dict(
  DESCRIPTOR = _TESTALLEXTENSIONS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestAllExtensions)

OptionalGroup_extension = _reflection.GeneratedProtocolMessageType('OptionalGroup_extension', (_message.Message,), dict(
  DESCRIPTOR = _OPTIONALGROUP_EXTENSION,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(OptionalGroup_extension)

RepeatedGroup_extension = _reflection.GeneratedProtocolMessageType('RepeatedGroup_extension', (_message.Message,), dict(
  DESCRIPTOR = _REPEATEDGROUP_EXTENSION,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(RepeatedGroup_extension)

TestNestedExtension = _reflection.GeneratedProtocolMessageType('TestNestedExtension', (_message.Message,), dict(
  DESCRIPTOR = _TESTNESTEDEXTENSION,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestNestedExtension)

TestRequired = _reflection.GeneratedProtocolMessageType('TestRequired', (_message.Message,), dict(
  DESCRIPTOR = _TESTREQUIRED,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestRequired)

TestRequiredForeign = _reflection.GeneratedProtocolMessageType('TestRequiredForeign', (_message.Message,), dict(
  DESCRIPTOR = _TESTREQUIREDFOREIGN,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestRequiredForeign)

TestForeignNested = _reflection.GeneratedProtocolMessageType('TestForeignNested', (_message.Message,), dict(
  DESCRIPTOR = _TESTFOREIGNNESTED,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestForeignNested)

TestEmptyMessage = _reflection.GeneratedProtocolMessageType('TestEmptyMessage', (_message.Message,), dict(
  DESCRIPTOR = _TESTEMPTYMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestEmptyMessage)

TestEmptyMessageWithExtensions = _reflection.GeneratedProtocolMessageType('TestEmptyMessageWithExtensions', (_message.Message,), dict(
  DESCRIPTOR = _TESTEMPTYMESSAGEWITHEXTENSIONS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestEmptyMessageWithExtensions)

TestMultipleExtensionRanges = _reflection.GeneratedProtocolMessageType('TestMultipleExtensionRanges', (_message.Message,), dict(
  DESCRIPTOR = _TESTMULTIPLEEXTENSIONRANGES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestMultipleExtensionRanges)

TestReallyLargeTagNumber = _reflection.GeneratedProtocolMessageType('TestReallyLargeTagNumber', (_message.Message,), dict(
  DESCRIPTOR = _TESTREALLYLARGETAGNUMBER,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestReallyLargeTagNumber)

TestRecursiveMessage = _reflection.GeneratedProtocolMessageType('TestRecursiveMessage', (_message.Message,), dict(
  DESCRIPTOR = _TESTRECURSIVEMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestRecursiveMessage)

TestMutualRecursionA = _reflection.GeneratedProtocolMessageType('TestMutualRecursionA', (_message.Message,), dict(
  DESCRIPTOR = _TESTMUTUALRECURSIONA,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestMutualRecursionA)

TestMutualRecursionB = _reflection.GeneratedProtocolMessageType('TestMutualRecursionB', (_message.Message,), dict(
  DESCRIPTOR = _TESTMUTUALRECURSIONB,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestMutualRecursionB)

TestDupFieldNumber = _reflection.GeneratedProtocolMessageType('TestDupFieldNumber', (_message.Message,), dict(

  Foo = _reflection.GeneratedProtocolMessageType('Foo', (_message.Message,), dict(
    DESCRIPTOR = _TESTDUPFIELDNUMBER_FOO,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,

  Bar = _reflection.GeneratedProtocolMessageType('Bar', (_message.Message,), dict(
    DESCRIPTOR = _TESTDUPFIELDNUMBER_BAR,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTDUPFIELDNUMBER,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestDupFieldNumber)
_sym_db.RegisterMessage(TestDupFieldNumber.Foo)
_sym_db.RegisterMessage(TestDupFieldNumber.Bar)

TestEagerMessage = _reflection.GeneratedProtocolMessageType('TestEagerMessage', (_message.Message,), dict(
  DESCRIPTOR = _TESTEAGERMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestEagerMessage)

TestLazyMessage = _reflection.GeneratedProtocolMessageType('TestLazyMessage', (_message.Message,), dict(
  DESCRIPTOR = _TESTLAZYMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestLazyMessage)

TestNestedMessageHasBits = _reflection.GeneratedProtocolMessageType('TestNestedMessageHasBits', (_message.Message,), dict(

  NestedMessage = _reflection.GeneratedProtocolMessageType('NestedMessage', (_message.Message,), dict(
    DESCRIPTOR = _TESTNESTEDMESSAGEHASBITS_NESTEDMESSAGE,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTNESTEDMESSAGEHASBITS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestNestedMessageHasBits)
_sym_db.RegisterMessage(TestNestedMessageHasBits.NestedMessage)

TestCamelCaseFieldNames = _reflection.GeneratedProtocolMessageType('TestCamelCaseFieldNames', (_message.Message,), dict(
  DESCRIPTOR = _TESTCAMELCASEFIELDNAMES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestCamelCaseFieldNames)

TestFieldOrderings = _reflection.GeneratedProtocolMessageType('TestFieldOrderings', (_message.Message,), dict(
  DESCRIPTOR = _TESTFIELDORDERINGS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestFieldOrderings)

TestExtremeDefaultValues = _reflection.GeneratedProtocolMessageType('TestExtremeDefaultValues', (_message.Message,), dict(
  DESCRIPTOR = _TESTEXTREMEDEFAULTVALUES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestExtremeDefaultValues)

SparseEnumMessage = _reflection.GeneratedProtocolMessageType('SparseEnumMessage', (_message.Message,), dict(
  DESCRIPTOR = _SPARSEENUMMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(SparseEnumMessage)

OneString = _reflection.GeneratedProtocolMessageType('OneString', (_message.Message,), dict(
  DESCRIPTOR = _ONESTRING,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(OneString)

MoreString = _reflection.GeneratedProtocolMessageType('MoreString', (_message.Message,), dict(
  DESCRIPTOR = _MORESTRING,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(MoreString)

OneBytes = _reflection.GeneratedProtocolMessageType('OneBytes', (_message.Message,), dict(
  DESCRIPTOR = _ONEBYTES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(OneBytes)

MoreBytes = _reflection.GeneratedProtocolMessageType('MoreBytes', (_message.Message,), dict(
  DESCRIPTOR = _MOREBYTES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(MoreBytes)

Int32Message = _reflection.GeneratedProtocolMessageType('Int32Message', (_message.Message,), dict(
  DESCRIPTOR = _INT32MESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(Int32Message)

Uint32Message = _reflection.GeneratedProtocolMessageType('Uint32Message', (_message.Message,), dict(
  DESCRIPTOR = _UINT32MESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(Uint32Message)

Int64Message = _reflection.GeneratedProtocolMessageType('Int64Message', (_message.Message,), dict(
  DESCRIPTOR = _INT64MESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(Int64Message)

Uint64Message = _reflection.GeneratedProtocolMessageType('Uint64Message', (_message.Message,), dict(
  DESCRIPTOR = _UINT64MESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(Uint64Message)

BoolMessage = _reflection.GeneratedProtocolMessageType('BoolMessage', (_message.Message,), dict(
  DESCRIPTOR = _BOOLMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(BoolMessage)

TestOneof = _reflection.GeneratedProtocolMessageType('TestOneof', (_message.Message,), dict(

  FooGroup = _reflection.GeneratedProtocolMessageType('FooGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTONEOF_FOOGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTONEOF,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestOneof)
_sym_db.RegisterMessage(TestOneof.FooGroup)

TestOneofBackwardsCompatible = _reflection.GeneratedProtocolMessageType('TestOneofBackwardsCompatible', (_message.Message,), dict(

  FooGroup = _reflection.GeneratedProtocolMessageType('FooGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTONEOFBACKWARDSCOMPATIBLE_FOOGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTONEOFBACKWARDSCOMPATIBLE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestOneofBackwardsCompatible)
_sym_db.RegisterMessage(TestOneofBackwardsCompatible.FooGroup)

TestOneof2 = _reflection.GeneratedProtocolMessageType('TestOneof2', (_message.Message,), dict(

  FooGroup = _reflection.GeneratedProtocolMessageType('FooGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTONEOF2_FOOGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,

  NestedMessage = _reflection.GeneratedProtocolMessageType('NestedMessage', (_message.Message,), dict(
    DESCRIPTOR = _TESTONEOF2_NESTEDMESSAGE,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTONEOF2,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestOneof2)
_sym_db.RegisterMessage(TestOneof2.FooGroup)
_sym_db.RegisterMessage(TestOneof2.NestedMessage)

TestRequiredOneof = _reflection.GeneratedProtocolMessageType('TestRequiredOneof', (_message.Message,), dict(

  NestedMessage = _reflection.GeneratedProtocolMessageType('NestedMessage', (_message.Message,), dict(
    DESCRIPTOR = _TESTREQUIREDONEOF_NESTEDMESSAGE,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTREQUIREDONEOF,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestRequiredOneof)
_sym_db.RegisterMessage(TestRequiredOneof.NestedMessage)

TestPackedTypes = _reflection.GeneratedProtocolMessageType('TestPackedTypes', (_message.Message,), dict(
  DESCRIPTOR = _TESTPACKEDTYPES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestPackedTypes)

TestUnpackedTypes = _reflection.GeneratedProtocolMessageType('TestUnpackedTypes', (_message.Message,), dict(
  DESCRIPTOR = _TESTUNPACKEDTYPES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestUnpackedTypes)

TestPackedExtensions = _reflection.GeneratedProtocolMessageType('TestPackedExtensions', (_message.Message,), dict(
  DESCRIPTOR = _TESTPACKEDEXTENSIONS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestPackedExtensions)

TestUnpackedExtensions = _reflection.GeneratedProtocolMessageType('TestUnpackedExtensions', (_message.Message,), dict(
  DESCRIPTOR = _TESTUNPACKEDEXTENSIONS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestUnpackedExtensions)

TestDynamicExtensions = _reflection.GeneratedProtocolMessageType('TestDynamicExtensions', (_message.Message,), dict(

  DynamicMessageType = _reflection.GeneratedProtocolMessageType('DynamicMessageType', (_message.Message,), dict(
    DESCRIPTOR = _TESTDYNAMICEXTENSIONS_DYNAMICMESSAGETYPE,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTDYNAMICEXTENSIONS,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestDynamicExtensions)
_sym_db.RegisterMessage(TestDynamicExtensions.DynamicMessageType)

TestRepeatedScalarDifferentTagSizes = _reflection.GeneratedProtocolMessageType('TestRepeatedScalarDifferentTagSizes', (_message.Message,), dict(
  DESCRIPTOR = _TESTREPEATEDSCALARDIFFERENTTAGSIZES,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestRepeatedScalarDifferentTagSizes)

TestParsingMerge = _reflection.GeneratedProtocolMessageType('TestParsingMerge', (_message.Message,), dict(

  RepeatedFieldsGenerator = _reflection.GeneratedProtocolMessageType('RepeatedFieldsGenerator', (_message.Message,), dict(

    Group1 = _reflection.GeneratedProtocolMessageType('Group1', (_message.Message,), dict(
      DESCRIPTOR = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP1,
      __module__ = 'google.protobuf.unittest_pb2'
      
      ))
    ,

    Group2 = _reflection.GeneratedProtocolMessageType('Group2', (_message.Message,), dict(
      DESCRIPTOR = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR_GROUP2,
      __module__ = 'google.protobuf.unittest_pb2'
      
      ))
    ,
    DESCRIPTOR = _TESTPARSINGMERGE_REPEATEDFIELDSGENERATOR,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,

  OptionalGroup = _reflection.GeneratedProtocolMessageType('OptionalGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTPARSINGMERGE_OPTIONALGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,

  RepeatedGroup = _reflection.GeneratedProtocolMessageType('RepeatedGroup', (_message.Message,), dict(
    DESCRIPTOR = _TESTPARSINGMERGE_REPEATEDGROUP,
    __module__ = 'google.protobuf.unittest_pb2'
    
    ))
  ,
  DESCRIPTOR = _TESTPARSINGMERGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestParsingMerge)
_sym_db.RegisterMessage(TestParsingMerge.RepeatedFieldsGenerator)
_sym_db.RegisterMessage(TestParsingMerge.RepeatedFieldsGenerator.Group1)
_sym_db.RegisterMessage(TestParsingMerge.RepeatedFieldsGenerator.Group2)
_sym_db.RegisterMessage(TestParsingMerge.OptionalGroup)
_sym_db.RegisterMessage(TestParsingMerge.RepeatedGroup)

TestCommentInjectionMessage = _reflection.GeneratedProtocolMessageType('TestCommentInjectionMessage', (_message.Message,), dict(
  DESCRIPTOR = _TESTCOMMENTINJECTIONMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(TestCommentInjectionMessage)

FooRequest = _reflection.GeneratedProtocolMessageType('FooRequest', (_message.Message,), dict(
  DESCRIPTOR = _FOOREQUEST,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(FooRequest)

FooResponse = _reflection.GeneratedProtocolMessageType('FooResponse', (_message.Message,), dict(
  DESCRIPTOR = _FOORESPONSE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(FooResponse)

FooClientMessage = _reflection.GeneratedProtocolMessageType('FooClientMessage', (_message.Message,), dict(
  DESCRIPTOR = _FOOCLIENTMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(FooClientMessage)

FooServerMessage = _reflection.GeneratedProtocolMessageType('FooServerMessage', (_message.Message,), dict(
  DESCRIPTOR = _FOOSERVERMESSAGE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(FooServerMessage)

BarRequest = _reflection.GeneratedProtocolMessageType('BarRequest', (_message.Message,), dict(
  DESCRIPTOR = _BARREQUEST,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(BarRequest)

BarResponse = _reflection.GeneratedProtocolMessageType('BarResponse', (_message.Message,), dict(
  DESCRIPTOR = _BARRESPONSE,
  __module__ = 'google.protobuf.unittest_pb2'
  
  ))
_sym_db.RegisterMessage(BarResponse)

TestAllExtensions.RegisterExtension(optional_int32_extension)
TestAllExtensions.RegisterExtension(optional_int64_extension)
TestAllExtensions.RegisterExtension(optional_uint32_extension)
TestAllExtensions.RegisterExtension(optional_uint64_extension)
TestAllExtensions.RegisterExtension(optional_sint32_extension)
TestAllExtensions.RegisterExtension(optional_sint64_extension)
TestAllExtensions.RegisterExtension(optional_fixed32_extension)
TestAllExtensions.RegisterExtension(optional_fixed64_extension)
TestAllExtensions.RegisterExtension(optional_sfixed32_extension)
TestAllExtensions.RegisterExtension(optional_sfixed64_extension)
TestAllExtensions.RegisterExtension(optional_float_extension)
TestAllExtensions.RegisterExtension(optional_double_extension)
TestAllExtensions.RegisterExtension(optional_bool_extension)
TestAllExtensions.RegisterExtension(optional_string_extension)
TestAllExtensions.RegisterExtension(optional_bytes_extension)
optionalgroup_extension.message_type = _OPTIONALGROUP_EXTENSION
TestAllExtensions.RegisterExtension(optionalgroup_extension)
optional_nested_message_extension.message_type = _TESTALLTYPES_NESTEDMESSAGE
TestAllExtensions.RegisterExtension(optional_nested_message_extension)
optional_foreign_message_extension.message_type = _FOREIGNMESSAGE
TestAllExtensions.RegisterExtension(optional_foreign_message_extension)
optional_import_message_extension.message_type = google.protobuf.unittest_import_pb2._IMPORTMESSAGE
TestAllExtensions.RegisterExtension(optional_import_message_extension)
optional_nested_enum_extension.enum_type = _TESTALLTYPES_NESTEDENUM
TestAllExtensions.RegisterExtension(optional_nested_enum_extension)
optional_foreign_enum_extension.enum_type = _FOREIGNENUM
TestAllExtensions.RegisterExtension(optional_foreign_enum_extension)
optional_import_enum_extension.enum_type = google.protobuf.unittest_import_pb2._IMPORTENUM
TestAllExtensions.RegisterExtension(optional_import_enum_extension)
TestAllExtensions.RegisterExtension(optional_string_piece_extension)
TestAllExtensions.RegisterExtension(optional_cord_extension)
optional_public_import_message_extension.message_type = google.protobuf.unittest_import_public_pb2._PUBLICIMPORTMESSAGE
TestAllExtensions.RegisterExtension(optional_public_import_message_extension)
optional_lazy_message_extension.message_type = _TESTALLTYPES_NESTEDMESSAGE
TestAllExtensions.RegisterExtension(optional_lazy_message_extension)
TestAllExtensions.RegisterExtension(repeated_int32_extension)
TestAllExtensions.RegisterExtension(repeated_int64_extension)
TestAllExtensions.RegisterExtension(repeated_uint32_extension)
TestAllExtensions.RegisterExtension(repeated_uint64_extension)
TestAllExtensions.RegisterExtension(repeated_sint32_extension)
TestAllExtensions.RegisterExtension(repeated_sint64_extension)
TestAllExtensions.RegisterExtension(repeated_fixed32_extension)
TestAllExtensions.RegisterExtension(repeated_fixed64_extension)
TestAllExtensions.RegisterExtension(repeated_sfixed32_extension)
TestAllExtensions.RegisterExtension(repeated_sfixed64_extension)
TestAllExtensions.RegisterExtension(repeated_float_extension)
TestAllExtensions.RegisterExtension(repeated_double_extension)
TestAllExtensions.RegisterExtension(repeated_bool_extension)
TestAllExtensions.RegisterExtension(repeated_string_extension)
TestAllExtensions.RegisterExtension(repeated_bytes_extension)
repeatedgroup_extension.message_type = _REPEATEDGROUP_EXTENSION
TestAllExtensions.RegisterExtension(repeatedgroup_extension)
repeated_nested_message_extension.message_type = _TESTALLTYPES_NESTEDMESSAGE
TestAllExtensions.RegisterExtension(repeated_nested_message_extension)
repeated_foreign_message_extension.message_type = _FOREIGNMESSAGE
TestAllExtensions.RegisterExtension(repeated_foreign_message_extension)
repeated_import_message_extension.message_type = google.protobuf.unittest_import_pb2._IMPORTMESSAGE
TestAllExtensions.RegisterExtension(repeated_import_message_extension)
repeated_nested_enum_extension.enum_type = _TESTALLTYPES_NESTEDENUM
TestAllExtensions.RegisterExtension(repeated_nested_enum_extension)
repeated_foreign_enum_extension.enum_type = _FOREIGNENUM
TestAllExtensions.RegisterExtension(repeated_foreign_enum_extension)
repeated_import_enum_extension.enum_type = google.protobuf.unittest_import_pb2._IMPORTENUM
TestAllExtensions.RegisterExtension(repeated_import_enum_extension)
TestAllExtensions.RegisterExtension(repeated_string_piece_extension)
TestAllExtensions.RegisterExtension(repeated_cord_extension)
repeated_lazy_message_extension.message_type = _TESTALLTYPES_NESTEDMESSAGE
TestAllExtensions.RegisterExtension(repeated_lazy_message_extension)
TestAllExtensions.RegisterExtension(default_int32_extension)
TestAllExtensions.RegisterExtension(default_int64_extension)
TestAllExtensions.RegisterExtension(default_uint32_extension)
TestAllExtensions.RegisterExtension(default_uint64_extension)
TestAllExtensions.RegisterExtension(default_sint32_extension)
TestAllExtensions.RegisterExtension(default_sint64_extension)
TestAllExtensions.RegisterExtension(default_fixed32_extension)
TestAllExtensions.RegisterExtension(default_fixed64_extension)
TestAllExtensions.RegisterExtension(default_sfixed32_extension)
TestAllExtensions.RegisterExtension(default_sfixed64_extension)
TestAllExtensions.RegisterExtension(default_float_extension)
TestAllExtensions.RegisterExtension(default_double_extension)
TestAllExtensions.RegisterExtension(default_bool_extension)
TestAllExtensions.RegisterExtension(default_string_extension)
TestAllExtensions.RegisterExtension(default_bytes_extension)
default_nested_enum_extension.enum_type = _TESTALLTYPES_NESTEDENUM
TestAllExtensions.RegisterExtension(default_nested_enum_extension)
default_foreign_enum_extension.enum_type = _FOREIGNENUM
TestAllExtensions.RegisterExtension(default_foreign_enum_extension)
default_import_enum_extension.enum_type = google.protobuf.unittest_import_pb2._IMPORTENUM
TestAllExtensions.RegisterExtension(default_import_enum_extension)
TestAllExtensions.RegisterExtension(default_string_piece_extension)
TestAllExtensions.RegisterExtension(default_cord_extension)
TestAllExtensions.RegisterExtension(oneof_uint32_extension)
oneof_nested_message_extension.message_type = _TESTALLTYPES_NESTEDMESSAGE
TestAllExtensions.RegisterExtension(oneof_nested_message_extension)
TestAllExtensions.RegisterExtension(oneof_string_extension)
TestAllExtensions.RegisterExtension(oneof_bytes_extension)
TestFieldOrderings.RegisterExtension(my_extension_string)
TestFieldOrderings.RegisterExtension(my_extension_int)
TestPackedExtensions.RegisterExtension(packed_int32_extension)
TestPackedExtensions.RegisterExtension(packed_int64_extension)
TestPackedExtensions.RegisterExtension(packed_uint32_extension)
TestPackedExtensions.RegisterExtension(packed_uint64_extension)
TestPackedExtensions.RegisterExtension(packed_sint32_extension)
TestPackedExtensions.RegisterExtension(packed_sint64_extension)
TestPackedExtensions.RegisterExtension(packed_fixed32_extension)
TestPackedExtensions.RegisterExtension(packed_fixed64_extension)
TestPackedExtensions.RegisterExtension(packed_sfixed32_extension)
TestPackedExtensions.RegisterExtension(packed_sfixed64_extension)
TestPackedExtensions.RegisterExtension(packed_float_extension)
TestPackedExtensions.RegisterExtension(packed_double_extension)
TestPackedExtensions.RegisterExtension(packed_bool_extension)
packed_enum_extension.enum_type = _FOREIGNENUM
TestPackedExtensions.RegisterExtension(packed_enum_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_int32_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_int64_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_uint32_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_uint64_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_sint32_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_sint64_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_fixed32_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_fixed64_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_sfixed32_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_sfixed64_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_float_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_double_extension)
TestUnpackedExtensions.RegisterExtension(unpacked_bool_extension)
unpacked_enum_extension.enum_type = _FOREIGNENUM
TestUnpackedExtensions.RegisterExtension(unpacked_enum_extension)
TestAllExtensions.RegisterExtension(_TESTNESTEDEXTENSION.extensions_by_name['test'])
TestAllExtensions.RegisterExtension(_TESTNESTEDEXTENSION.extensions_by_name['nested_string_extension'])
_TESTREQUIRED.extensions_by_name['single'].message_type = _TESTREQUIRED
TestAllExtensions.RegisterExtension(_TESTREQUIRED.extensions_by_name['single'])
_TESTREQUIRED.extensions_by_name['multi'].message_type = _TESTREQUIRED
TestAllExtensions.RegisterExtension(_TESTREQUIRED.extensions_by_name['multi'])
_TESTPARSINGMERGE.extensions_by_name['optional_ext'].message_type = _TESTALLTYPES
TestParsingMerge.RegisterExtension(_TESTPARSINGMERGE.extensions_by_name['optional_ext'])
_TESTPARSINGMERGE.extensions_by_name['repeated_ext'].message_type = _TESTALLTYPES
TestParsingMerge.RegisterExtension(_TESTPARSINGMERGE.extensions_by_name['repeated_ext'])

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\rUnittestProtoH\001\200\001\001\210\001\001\220\001\001'))
_TESTENUMWITHDUPVALUE.has_options = True
_TESTENUMWITHDUPVALUE._options = _descriptor._ParseOptions(descriptor_pb2.EnumOptions(), _b('\020\001'))
optional_string_piece_extension.has_options = True
optional_string_piece_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
optional_cord_extension.has_options = True
optional_cord_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
optional_lazy_message_extension.has_options = True
optional_lazy_message_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))
repeated_string_piece_extension.has_options = True
repeated_string_piece_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
repeated_cord_extension.has_options = True
repeated_cord_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
repeated_lazy_message_extension.has_options = True
repeated_lazy_message_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))
default_string_piece_extension.has_options = True
default_string_piece_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
default_cord_extension.has_options = True
default_cord_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
packed_int32_extension.has_options = True
packed_int32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_int64_extension.has_options = True
packed_int64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_uint32_extension.has_options = True
packed_uint32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_uint64_extension.has_options = True
packed_uint64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_sint32_extension.has_options = True
packed_sint32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_sint64_extension.has_options = True
packed_sint64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_fixed32_extension.has_options = True
packed_fixed32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_fixed64_extension.has_options = True
packed_fixed64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_sfixed32_extension.has_options = True
packed_sfixed32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_sfixed64_extension.has_options = True
packed_sfixed64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_float_extension.has_options = True
packed_float_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_double_extension.has_options = True
packed_double_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_bool_extension.has_options = True
packed_bool_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
packed_enum_extension.has_options = True
packed_enum_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
unpacked_int32_extension.has_options = True
unpacked_int32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_int64_extension.has_options = True
unpacked_int64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_uint32_extension.has_options = True
unpacked_uint32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_uint64_extension.has_options = True
unpacked_uint64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_sint32_extension.has_options = True
unpacked_sint32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_sint64_extension.has_options = True
unpacked_sint64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_fixed32_extension.has_options = True
unpacked_fixed32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_fixed64_extension.has_options = True
unpacked_fixed64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_sfixed32_extension.has_options = True
unpacked_sfixed32_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_sfixed64_extension.has_options = True
unpacked_sfixed64_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_float_extension.has_options = True
unpacked_float_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_double_extension.has_options = True
unpacked_double_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_bool_extension.has_options = True
unpacked_bool_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
unpacked_enum_extension.has_options = True
unpacked_enum_extension._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTALLTYPES.fields_by_name['optional_string_piece'].has_options = True
_TESTALLTYPES.fields_by_name['optional_string_piece']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTALLTYPES.fields_by_name['optional_cord'].has_options = True
_TESTALLTYPES.fields_by_name['optional_cord']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTALLTYPES.fields_by_name['optional_lazy_message'].has_options = True
_TESTALLTYPES.fields_by_name['optional_lazy_message']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))
_TESTALLTYPES.fields_by_name['repeated_string_piece'].has_options = True
_TESTALLTYPES.fields_by_name['repeated_string_piece']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTALLTYPES.fields_by_name['repeated_cord'].has_options = True
_TESTALLTYPES.fields_by_name['repeated_cord']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTALLTYPES.fields_by_name['repeated_lazy_message'].has_options = True
_TESTALLTYPES.fields_by_name['repeated_lazy_message']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))
_TESTALLTYPES.fields_by_name['default_string_piece'].has_options = True
_TESTALLTYPES.fields_by_name['default_string_piece']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTALLTYPES.fields_by_name['default_cord'].has_options = True
_TESTALLTYPES.fields_by_name['default_cord']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTDEPRECATEDFIELDS.fields_by_name['deprecated_int32'].has_options = True
_TESTDEPRECATEDFIELDS.fields_by_name['deprecated_int32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\030\001'))
_TESTEAGERMESSAGE.fields_by_name['sub_message'].has_options = True
_TESTEAGERMESSAGE.fields_by_name['sub_message']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\000'))
_TESTLAZYMESSAGE.fields_by_name['sub_message'].has_options = True
_TESTLAZYMESSAGE.fields_by_name['sub_message']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))
_TESTCAMELCASEFIELDNAMES.fields_by_name['StringPieceField'].has_options = True
_TESTCAMELCASEFIELDNAMES.fields_by_name['StringPieceField']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTCAMELCASEFIELDNAMES.fields_by_name['CordField'].has_options = True
_TESTCAMELCASEFIELDNAMES.fields_by_name['CordField']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTCAMELCASEFIELDNAMES.fields_by_name['RepeatedStringPieceField'].has_options = True
_TESTCAMELCASEFIELDNAMES.fields_by_name['RepeatedStringPieceField']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTCAMELCASEFIELDNAMES.fields_by_name['RepeatedCordField'].has_options = True
_TESTCAMELCASEFIELDNAMES.fields_by_name['RepeatedCordField']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTEXTREMEDEFAULTVALUES.fields_by_name['string_piece_with_zero'].has_options = True
_TESTEXTREMEDEFAULTVALUES.fields_by_name['string_piece_with_zero']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTEXTREMEDEFAULTVALUES.fields_by_name['cord_with_zero'].has_options = True
_TESTEXTREMEDEFAULTVALUES.fields_by_name['cord_with_zero']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTONEOF2.fields_by_name['foo_cord'].has_options = True
_TESTONEOF2.fields_by_name['foo_cord']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTONEOF2.fields_by_name['foo_string_piece'].has_options = True
_TESTONEOF2.fields_by_name['foo_string_piece']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTONEOF2.fields_by_name['foo_lazy_message'].has_options = True
_TESTONEOF2.fields_by_name['foo_lazy_message']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('(\001'))
_TESTONEOF2.fields_by_name['bar_cord'].has_options = True
_TESTONEOF2.fields_by_name['bar_cord']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\001'))
_TESTONEOF2.fields_by_name['bar_string_piece'].has_options = True
_TESTONEOF2.fields_by_name['bar_string_piece']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\010\002'))
_TESTPACKEDTYPES.fields_by_name['packed_int32'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_int32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_int64'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_int64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_uint32'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_uint32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_uint64'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_uint64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_sint32'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_sint32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_sint64'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_sint64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_fixed32'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_fixed32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_fixed64'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_fixed64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_sfixed32'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_sfixed32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_sfixed64'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_sfixed64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_float'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_float']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_double'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_double']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_bool'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_bool']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTPACKEDTYPES.fields_by_name['packed_enum'].has_options = True
_TESTPACKEDTYPES.fields_by_name['packed_enum']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_int32'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_int32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_int64'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_int64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_uint32'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_uint32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_uint64'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_uint64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sint32'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sint32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sint64'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sint64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_fixed32'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_fixed32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_fixed64'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_fixed64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sfixed32'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sfixed32']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sfixed64'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_sfixed64']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_float'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_float']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_double'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_double']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_bool'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_bool']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTUNPACKEDTYPES.fields_by_name['unpacked_enum'].has_options = True
_TESTUNPACKEDTYPES.fields_by_name['unpacked_enum']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\000'))
_TESTDYNAMICEXTENSIONS.fields_by_name['packed_extension'].has_options = True
_TESTDYNAMICEXTENSIONS.fields_by_name['packed_extension']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))

_TESTSERVICE = _descriptor.ServiceDescriptor(
  name='TestService',
  full_name='protobuf_unittest.TestService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=12477,
  serialized_end=12630,
  methods=[
  _descriptor.MethodDescriptor(
    name='Foo',
    full_name='protobuf_unittest.TestService.Foo',
    index=0,
    containing_service=None,
    input_type=_FOOREQUEST,
    output_type=_FOORESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Bar',
    full_name='protobuf_unittest.TestService.Bar',
    index=1,
    containing_service=None,
    input_type=_BARREQUEST,
    output_type=_BARRESPONSE,
    options=None,
  ),
])

TestService = service_reflection.GeneratedServiceType('TestService', (_service.Service,), dict(
  DESCRIPTOR = _TESTSERVICE,
  __module__ = 'google.protobuf.unittest_pb2'
  ))

TestService_Stub = service_reflection.GeneratedServiceStubType('TestService_Stub', (TestService,), dict(
  DESCRIPTOR = _TESTSERVICE,
  __module__ = 'google.protobuf.unittest_pb2'
  ))




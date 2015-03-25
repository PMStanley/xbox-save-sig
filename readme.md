# Xbox Save Sig

The original Xbox (2001) has cryptographically signed saves, to edit or manipulate them you need to be able to resign the save with the games unique key.
This key is generated using 2 input sources, the master Xbox key and the games unique signing key.  

xboxsig.py is a python utility to generate the keys used for resigning saves.

## Basic Usage

The minimum information you need to supply to xboxsig.py is the games executable file (default.xbe) or a text representation of the games signature key:

```python xboxsig.py -i /path/to/default.xbe```

or

```python xboxsig.py -g E34B1AE87CDE555DC5A5CC7E30DDAACE```

The output will be a text representation of the digital signature for save signing: `737E064C0236BA3E7140EC2B91D76766`

## Advanced Options

Additional parameters can be supplied on the command line:

option | result
-------|-------
`-t` | Outputs the Title Name from the default.xbe file in addition to the signature.  Has no effect if the -g option is used in place of -i
`-o <filename>` | Outputs to the supplied file instead of the console
`-f <format>` | Outputs the key in a specified format, valid options are covered in the Output Format section
`-x <Xbox key in text form>` | Use the Xbox key supplied on the command line instead of the master key.  Should not be used unless you have a specific need to change Xbox key

## Output Format
The save signing key is calculated as a 20 byte digest but only the first 16 bytes are used when signing files.
There are 3 options for the output format, the default is 'native' and is used if this option is skipped.

Format | Description | format
-------|------------
native | Key is displayed as a 16 byte signature | 737E064C0236BA3E7140EC2B91D76766
raw | Full 20 byte digest | 737E064C0236BA3E7140EC2B91D76766C1F4B510
xbtf | Xbox Trainer Format | 0X73, 0X7E, 0X06, 0X4C, 0X02, 0X36, 0XBA, 0X3E, 0X71, 0X40, 0XEC, 0X2B, 0X91, 0XD7, 0X67, 0X66

Example:
```python xboxsig.py -i default.xbe -f xbtf```

Output:
`0X73, 0X7E, 0X06, 0X4C, 0X02, 0X36, 0XBA, 0X3E, 0X71, 0X40, 0XEC, 0X2B, 0X91, 0XD7, 0X67, 0X66`

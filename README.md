# interceptor
[![Maintainability](https://api.codeclimate.com/v1/badges/8e423b83128c001fc6a2/maintainability)](https://codeclimate.com/github/Cervi-Robotics/interceptor/maintainability)

A tool to intercept calls to your command line tools and alter their args.

Requires UNIX and working Python3 and whereis.

## Installation

Since the `interceptor` PyPI package name is taken, 
you ought to install interceptor the following way:

```bash
pip install git+https://github.com/Cervi-Robotics/interceptor.git
```

Or, if you don't have pip:

```bash
git clone https://github.com/Cervi-Robotics/interceptor.git
cd interceptor
python setup.py install
```

## Usage

### Prepare the configuration

To override g++ put a JSON file at `/etc/interceptor.d/g++`

with the following contents:

```json
{
  "args_to_disable": ["-quiet"],
  "args_to_append": ["-DDEBUG"]],
  "args_to_prepend": ["-v"],
  "args_to_replace": [["-march=native", "-mcpu=native"]],
  "display_before_start": true,
  "notify_about_actions": false
}
```

#### Configuring

If the intercepted command sees any arguments given in 
`args_to_disable` they will be removed before being passed to target command.

If arguments in `args_to_append` are not in arguments, 
they will be appended to the arguments.

The arguments in `args_to_append` will be appended in the order they are listed.

If arguments in `args_to_prepend` are not in arguments,
they will be prepended to arguments.

The arguments in `args_to_prepend` will be appended in the order they are listed.

You give two-item lists in `args_to_replace`. If
the first item occurs in arguments, it will be replaced by the second item. 

If you don't prepare the configuration file in advance, an empty file will be created for you.
     
If `display_before_start` is set, then before the launch
the application name and parameters actually passed to it will be displayed on stdout.
     
If `notify_about_actions` is set, then interceptor will print out
each case an action is attempted.     
     
### The intercept command

The `intercept` command is the basic command used to interface with interceptor.

#### Intercepting tools

Say, to intercept the command `foo` invoke:

```bash
intercept foo
```

Interceptor should display the following:

```
Successfully intercepted foo
```

Note that you will be unable to proceed if foo is already an interceptor wrapper.

A Python wrapper will be found at previous location of 
foo, while it itself will be copied to the same directory
but named `foo-intercepted`.
The wrapper will hold the name of `foo` inside, 
so you can symlink it safely (eg. symlink of g++ to c++).

To cancel intercepting `foo` type:

```bash
intercept undo foo
```

To check whether `foo` is being intercepted type:

```bash
intercept status foo
```

To provide configuration for `foo` type

```bash
intercept configure foo```
```
And type in the configuration in JSON format, followed by Ctrl+D.

To display current configuration for `foo` type:

```bash
intercept show foo
``` 

To have intercept display when the tool is called type:
```bash
intercept display foo
```

To hide the display type:
```bash
intercept hide foo
```

To have nano/vi run to edit your config file type:
```bash
intercept edit foo
```

To add an argument to be appended to the command type:

```bash
intercept append foo arg
```

To add an argument to be prepended to the command type:

```bash
intercept prepend foo arg
```

To add an argument to be elliminated if foo is called with it
type:

```bash
intercept disable foo arg
```

To replace arg1 with arg2 each time foo is called type:

```bash
intercept replace foo arg1 arg2
```

To have intercept display when an action is taken type:
```bash
intercept notify foo
```

To hide the notifications type:
```bash
intercept unnotify foo
```

To symlink bar's configuration to that of foo type:

```bash
intercept link foo bar
```

To copy foo's configuration to that of bar type:

```bash
intercept copy foo bar
```


Note that intercept will refuse to link to foo if foo is already a symlink.
To circumvent that type:
```bash
intercept link foo bar --force
```

To reset configuration of foo, type
```bash
intercept reset foo
```

Note that this will unlink foo is it is already a symlink.

If you seek only to validate foo's config, type:
```bash
intercept check foo
```
It will be additionally reformatted.

# Create a Linux user

## 1. Create user

### `useradd -m -s /bin/bash <username>`

* The `-m` flag specifies that the **home directory** should be created and it will be in the standard location of `/home/<username>`. Without this flag, no home directory is created
* If you want a different location, you can add a `-d <directory>` argument.
* `-s /bin/bash` sets the default shell for this user

## 2. Set the password

### `passwd username`

## 3. Copy the SSH key into the user's home directory

### `cp ~/.ssh/authorized_keys /home/<username>/.ssh/`
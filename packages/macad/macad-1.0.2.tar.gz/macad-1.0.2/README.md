# Macad
The Tool For Changing Your MAC Address for Any Interface

To install this package, use

```bash
sudo pip install macad
```
> Note: `this library requires root privileges, you need to use sudo`

## RUN

Want to contribute? Great!

Open your favorite Terminal and run these commands.

See All Arguments and Options for more information:

```sh
sudo macad -h
```

Find your interface and put cammand

```sh
sudo macad -i <interface> -m <new mac address>
OR 
sudo macad --interface <interface> --mac <new mac address>
```

Example:

```sh
sudo macad -i wp2s1 -m 00:11:22:33:44:55
```
> Note: `sometimes assigned mac not be available so for that start mac from 00:XX:XX:XX:XX:XX`

The output  look like this

```sh
[+] MAC Address was Successfully Changed to 00:XX:XX:XX:XX:XX

```

## License

MIT

**Free Software, Hell Yeah!**

## Author

[Deepak Patidar](https://github.com/DeepakDarkiee/great-text)
# HID Repro

We've encountered some issues with some HID Omnikey card readers. We initially documented this here:

https://gist.github.com/eventualbuddha/d0c5c70480dc4d22deb4054ac11535fc

We've since narrowed down the issue a little bit more.

First, regarding card reader models:
* Faulty card readers are OMNIKEY 3021 (rev C 2021) or OMNIKEY 3121 (rev A 2017).
* Good card readers are OMNIKEY 3021 (rev A 2016) or OMNIKEY 3121 (rev A 2016).

Then, reproduce the issue with this python program. You'll need Python 3.8 and pipenv.

```
pipenv install
```

Then, plug in a reader and insert an AT24C64 card into it.

Run the script to reproduce the issue as follows:


```
pipenv run python repro.py
```

With a good card reader, all writes-and-reads, at address 0x00 or 0x20, length 32, 64, or more, should work just fine.

With a faulty card reader, write-and-read at address 0x00 longer than 32 bytes, or write-and-read at address 0x20 longer than 64 bytes, will fail to return the same value written.

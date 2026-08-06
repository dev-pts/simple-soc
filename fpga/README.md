Tried Tang Primer 25K and gowin IDE.

* Needed to set option for dual pin CPU and add CLK pin, otherwise no clock.
* ILA is GOA.
* Needed to use WINUSB driver in GOA.
* Programmer in IDE did not work. Programmer in GOA worked just fine.
* BRAMs and their dual-port-able are strange.
* UART works bad. uart_out is working, but no data in minicom.
  Only USB unplug+plug helps.

To upload bitstream, git clone openFPGALoader, build and then:
```
./openFPGALoader -b tangprimer25k fpga_project.fs
```

To upload the fw:
```
python3 fpga/fw-upload.py -d /dev/ttyUSB1 -f fw/src/build/fw.bin
```

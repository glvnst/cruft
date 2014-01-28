# shlibs

python module recursively finds app library dependencies, optionally can make a chroot jail with this info

The [man page dyld](https://developer.apple.com/library/mac/documentation/Darwin/Reference/Manpages/man1/dyld.1.html) is an extremely useful reference for OS X / Darwin.

See [the blog post about mkjail](http://galvanist.com/post/56925855686/chroot-jails-on-os-x) for a little more about this project.

I'll get this project cleaned up... one day.


## Examples

### Programs in the examples directory

There are a few different programs in the examples directory that show how to use shlibs.

#### dyld_entries.py

otool -L doesn't tell you everything. This program shows the dynamic libraries referenced by a binary file, and whether the references are weak. See below the entry for the `SenTestingKit.framework`

	% ./dyld_entries.py /Applications/Bento.app/Contents/MacOS/Bento
	/Applications/Bento.app/Contents/MacOS/Bento:
	  /System/Library/Frameworks/AddressBook.framework/Versions/A/AddressBook
	  weak-ref:@rpath/SenTestingKit.framework/Versions/A/SenTestingKit
	  weak-ref:@rpath/GNDebugManager.framework/Versions/A/GNDebugManager
	  @rpath/Meta.framework/Versions/A/Meta
	  @rpath/GNPresentation.framework/Versions/A/GNPresentation
	  @rpath/GNControls.framework/Versions/A/GNControls
	  @rpath/GNUtility.framework/Versions/A/GNUtility
	  @rpath/GNDataManager.framework/Versions/A/GNDataManager
	  @rpath/GNCalculations.framework/Versions/A/GNCalculations
	  /System/Library/Frameworks/QTKit.framework/Versions/A/QTKit
	  /System/Library/Frameworks/ExceptionHandling.framework/Versions/A/ExceptionHandling
	  /System/Library/Frameworks/Quartz.framework/Versions/A/Quartz
	  /System/Library/Frameworks/QuartzCore.framework/Versions/A/QuartzCore
	  /System/Library/Frameworks/SystemConfiguration.framework/Versions/A/SystemConfiguration
	  /System/Library/Frameworks/AppKit.framework/Versions/C/AppKit
	  /System/Library/Frameworks/CoreData.framework/Versions/A/CoreData
	  /System/Library/Frameworks/Foundation.framework/Versions/C/Foundation
	  /System/Library/Frameworks/Quartz.framework/Versions/A/Frameworks/PDFKit.framework/Versions/A/PDFKit
	  /System/Library/Frameworks/QuickTime.framework/Versions/A/QuickTime
	  /System/Library/Frameworks/ApplicationServices.framework/Versions/A/ApplicationServices
	  /System/Library/Frameworks/Carbon.framework/Versions/A/Carbon
	  /System/Library/Frameworks/Cocoa.framework/Versions/A/Cocoa
	  /System/Library/Frameworks/WebKit.framework/Versions/A/WebKit
	  /usr/lib/libcrypto.0.9.8.dylib
	  /usr/lib/libsqlite3.dylib
	  /usr/lib/libz.1.dylib
	  /System/Library/Frameworks/Security.framework/Versions/A/Security
	  /System/Library/Frameworks/IOKit.framework/Versions/A/IOKit
	  /usr/lib/libstdc++.6.dylib
	  /usr/lib/libSystem.B.dylib
	  /usr/lib/libobjc.A.dylib
	  /System/Library/Frameworks/CoreServices.framework/Versions/A/CoreServices
	  /System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation

#### rpath_entries.py

One really important bit of information about some binary files is their list of runpath entries. These are used to resolve @rpath references. This program tells you the runpath entries listed in a binary file. 

	% ./rpath_entries.py /Applications/Bento.app/Contents/MacOS/Bento
	/Applications/Bento.app/Contents/MacOS/Bento:
	  '@executable_path/../Frameworks'
	  '/Applications/Xcode.app/Contents/Developer/Library/Frameworks'

#### mkjail.py

To run programs in a chroot jail, you need to have *all* the dependencies of your programs. The shlibs module is extremely helpful for gathering those.
See [the blog post about mkjail](http://galvanist.com/post/56925855686/chroot-jails-on-os-x) for a little more about this project.


### Using the module directly on the python command line

	% python -mshlibs --help
	usage: -mshlibs [-h] [-a] file [file ...]
	
	Print the complete list of shared libraries used by the specified binary
	file(s), (optionally including all child dependencies)
	
	positional arguments:
	  file        file(s) to report on
	
	optional arguments:
	  -h, --help  show this help message and exit
	  -a, --all   recursively resolve all sub-dependencies

#### /bin/ls and dependencies on OS X

To print the libraries referenced by an app, you can use the module directly on the command-line.

	% python -m shlibs /bin/ls
	/usr/lib/libSystem.B.dylib
	/usr/lib/libncurses.5.4.dylib
	/usr/lib/libutil.dylib

But this doesn't really show the whole picture. Because those dylibs have dependencies. We can add the '--all' flag to see the dependencies of the dependencies and their dependencies and so on.

	% python -m shlibs --all /bin/ls
	/bin/ls
	/usr/lib/libSystem.B.dylib
	/usr/lib/libc++.1.dylib
	/usr/lib/libc++abi.dylib
	/usr/lib/libncurses.5.4.dylib
	/usr/lib/libutil.dylib
	/usr/lib/system/libcache.dylib
	/usr/lib/system/libcommonCrypto.dylib
	/usr/lib/system/libcompiler_rt.dylib
	/usr/lib/system/libcopyfile.dylib
	/usr/lib/system/libcorecrypto.dylib
	/usr/lib/system/libdispatch.dylib
	/usr/lib/system/libdyld.dylib
	/usr/lib/system/libkeymgr.dylib
	/usr/lib/system/liblaunch.dylib
	/usr/lib/system/libmacho.dylib
	/usr/lib/system/libquarantine.dylib
	/usr/lib/system/libremovefile.dylib
	/usr/lib/system/libsystem_asl.dylib
	/usr/lib/system/libsystem_blocks.dylib
	/usr/lib/system/libsystem_c.dylib
	/usr/lib/system/libsystem_configuration.dylib
	/usr/lib/system/libsystem_dnssd.dylib
	/usr/lib/system/libsystem_info.dylib
	/usr/lib/system/libsystem_kernel.dylib
	/usr/lib/system/libsystem_m.dylib
	/usr/lib/system/libsystem_malloc.dylib
	/usr/lib/system/libsystem_network.dylib
	/usr/lib/system/libsystem_notify.dylib
	/usr/lib/system/libsystem_platform.dylib
	/usr/lib/system/libsystem_pthread.dylib
	/usr/lib/system/libsystem_sandbox.dylib
	/usr/lib/system/libsystem_stats.dylib
	/usr/lib/system/libunc.dylib
	/usr/lib/system/libunwind.dylib
	/usr/lib/system/libxpc.dylib

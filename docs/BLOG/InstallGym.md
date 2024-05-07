# 安装gym遇到的问题

```python
pip install gym==0.18.3
Collecting gym==0.18.3
  Using cached gym-0.18.3-py3-none-any.whl
Collecting scipy (from gym==0.18.3)
  Using cached scipy-1.10.1-cp38-cp38-macosx_12_0_arm64.whl.metadata (53 kB)
Collecting numpy>=1.10.4 (from gym==0.18.3)
  Using cached numpy-1.24.4-cp38-cp38-macosx_11_0_arm64.whl.metadata (5.6 kB)
Collecting pyglet<=1.5.15,>=1.4.0 (from gym==0.18.3)
  Using cached pyglet-1.5.15-py3-none-any.whl.metadata (7.6 kB)
Collecting Pillow<=8.2.0 (from gym==0.18.3)
  Using cached Pillow-8.2.0.tar.gz (47.9 MB)
  Preparing metadata (setup.py) ... done
Collecting cloudpickle<1.7.0,>=1.2.0 (from gym==0.18.3)
  Using cached cloudpickle-1.6.0-py3-none-any.whl.metadata (4.3 kB)
Using cached cloudpickle-1.6.0-py3-none-any.whl (23 kB)
Using cached numpy-1.24.4-cp38-cp38-macosx_11_0_arm64.whl (13.8 MB)
Using cached pyglet-1.5.15-py3-none-any.whl (1.1 MB)
Using cached scipy-1.10.1-cp38-cp38-macosx_12_0_arm64.whl (28.8 MB)
Building wheels for collected packages: Pillow
  Building wheel for Pillow (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [175 lines of output]
      running bdist_wheel
      running build
      running build_py
      creating build
      creating build/lib.macosx-11.1-arm64-3.8
      creating build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/MpoImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageMode.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PngImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/XbmImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PcxImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/SunImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/SpiderImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/TarIO.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/FitsStubImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/MpegImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/BdfFontFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/GribStubImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageStat.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PixarImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/GimpPaletteFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageColor.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ContainerIO.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/MspImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/MicImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/_version.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImtImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/GifImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PalmImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageQt.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageMath.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PaletteFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/FontFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PdfParser.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ExifTags.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageCms.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/FpxImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageChops.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/BufrStubImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PSDraw.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PcdImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageFilter.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageDraw2.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImagePath.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/DcxImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/__init__.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/JpegPresets.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/Hdf5StubImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/features.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageDraw.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/GimpGradientFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageWin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/IcoImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/_tkinter_finder.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/EpsImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/TgaImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageMorph.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/Jpeg2KImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/WalImageFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PcfFontFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/BlpImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageTk.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/GbrImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageOps.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PdfImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageShow.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageEnhance.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/WmfImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageGrab.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/WebPImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/FliImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/TiffTags.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/CurImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/_util.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/GdImageFile.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/TiffImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/IptcImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImagePalette.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/BmpImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageTransform.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/IcnsImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/McIdasImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/XpmImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/DdsImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageSequence.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PyAccess.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/_binary.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/Image.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/__main__.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/XVThumbImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/SgiImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PsdImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/JpegImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/ImageFont.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/PpmImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      copying src/PIL/FtexImagePlugin.py -> build/lib.macosx-11.1-arm64-3.8/PIL
      running egg_info
      writing src/Pillow.egg-info/PKG-INFO
      writing dependency_links to src/Pillow.egg-info/dependency_links.txt
      writing top-level names to src/Pillow.egg-info/top_level.txt
      reading manifest file 'src/Pillow.egg-info/SOURCES.txt'
      reading manifest template 'MANIFEST.in'
      warning: no files found matching '*.c'
      warning: no files found matching '*.h'
      warning: no files found matching '*.sh'
      warning: no previously-included files found matching '.appveyor.yml'
      warning: no previously-included files found matching '.clang-format'
      warning: no previously-included files found matching '.coveragerc'
      warning: no previously-included files found matching '.editorconfig'
      warning: no previously-included files found matching '.readthedocs.yml'
      warning: no previously-included files found matching 'codecov.yml'
      warning: no previously-included files matching '.git*' found anywhere in distribution
      warning: no previously-included files matching '*.pyc' found anywhere in distribution
      warning: no previously-included files matching '*.so' found anywhere in distribution
      no previously-included directories found matching '.ci'
      adding license file 'LICENSE'
      writing manifest file 'src/Pillow.egg-info/SOURCES.txt'
      running build_ext
      
      
      The headers or library files could not be found for jpeg,
      a required dependency when compiling Pillow from source.
      
      Please see the install instructions at:
         https://pillow.readthedocs.io/en/latest/installation.html
      
      Traceback (most recent call last):
        File "/private/var/folders/bq/5w8fylf939b65_qjwq96fvp00000gn/T/pip-install-3cl3ntrg/pillow_4e4dd253e97c4ca08e88d0b7950d37de/setup.py", line 976, in <module>
          setup(
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/site-packages/setuptools/__init__.py", line 153, in setup
          return distutils.core.setup(**attrs)
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/core.py", line 148, in setup
          dist.run_commands()
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/dist.py", line 966, in run_commands
          self.run_command(cmd)
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/dist.py", line 985, in run_command
          cmd_obj.run()
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/site-packages/wheel/bdist_wheel.py", line 299, in run
          self.run_command('build')
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/cmd.py", line 313, in run_command
          self.distribution.run_command(command)
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/dist.py", line 985, in run_command
          cmd_obj.run()
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/command/build.py", line 135, in run
          self.run_command(cmd_name)
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/cmd.py", line 313, in run_command
          self.distribution.run_command(command)
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/dist.py", line 985, in run_command
          cmd_obj.run()
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/site-packages/setuptools/command/build_ext.py", line 79, in run
          _build_ext.run(self)
        File "/Users/liuyu/anaconda3/envs/newgymlab/lib/python3.8/distutils/command/build_ext.py", line 340, in run
          self.build_extensions()
        File "/private/var/folders/bq/5w8fylf939b65_qjwq96fvp00000gn/T/pip-install-3cl3ntrg/pillow_4e4dd253e97c4ca08e88d0b7950d37de/setup.py", line 788, in build_extensions
          raise RequiredDependencyException(f)
      __main__.RequiredDependencyException: jpeg
      
      During handling of the above exception, another exception occurred:
      
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
        File "<pip-setuptools-caller>", line 34, in <module>
        File "/private/var/folders/bq/5w8fylf939b65_qjwq96fvp00000gn/T/pip-install-3cl3ntrg/pillow_4e4dd253e97c4ca08e88d0b7950d37de/setup.py", line 1033, in <module>
          raise RequiredDependencyException(msg)
      __main__.RequiredDependencyException:
      
      The headers or library files could not be found for jpeg,
      a required dependency when compiling Pillow from source.
      
      Please see the install instructions at:
         https://pillow.readthedocs.io/en/latest/installation.html
      
      
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for Pillow
  Running setup.py clean for Pillow
Failed to build Pillow
ERROR: Could not build wheels for Pillow, which is required to install pyproject.toml-based projects
```



在M1芯片上使用conda环境安装Pillow可能需要一些额外的步骤。你可以尝试以下方法来解决问题：

1. **安装依赖项：** 在conda环境中安装libjpeg-turbo包。你可以使用以下命令：

```bash
conda install libjpeg-turbo
```

2. **尝试重新安装Pillow：** 安装libjpeg-turbo后，再次尝试安装Pillow。

```bash
pip install --no-cache-dir pillow==8.2.0
```

如果这些步骤仍然无法解决问题，请确保你的环境和依赖项配置正确，或者尝试查看相关文档或论坛帖子，看看是否有其他人遇到了类似的问题。
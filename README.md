## Shared Advertising Board

广告屏作为智能城市服务，通过iExec的markert，运行DApp播放广告内容。

* 文件目录说明：
  
  \|--source: 程序源文件
  
  |    |----- customImage: 下载并存储用户广告的目录，播放slot timeout之后会自动清除 。
  
  |    |----- defaultImage: 存放默认界面的文件夹，包括两个背景图片和广告模板。
  
  |    |----- electronicScreen.py 屏幕端主程序
  
  |    |----- mqtt  广告发布端
  
  |    |-------\|---- publish.py 通过mqtt向屏幕发布广告的程序
  
  \|--UIDesign: 界面图片文件夹。包括空闲时切换的中英文背景图片
  
  |---|---background.jpg  默认界面
  
  |---|---backgroundCHN.jpg   默认界面中文
  
  |---|---ad_template.jpg   广告展示时的模板



* 屏幕端运行环境 
  
  linux, python3.5
  
  package requirement:
  
  -----
  
  paho-mqtt==1.4.0
  
  Pillow==6.0.0
  PyQt5==5.12.1
  PyQt5-sip==4.19.15

* 使用说明：
  
  * 屏幕端：
    
    ```bash
    cd ./source
    python3.5 electronicScreen.py
    ```
  
  * 发布内容：
    
    首先准备好图片URL，支持常见格式，可以使用 [file.io](https://www.file.io)上传图片,获得URL
    
    * 方法1:  运行
      
      ```bash
      cd ./mqtt
      
      python publish.py <ID> <URL>
      ```
      
      
    
    * docker 运行`docker run daleshen/ad_screen:V1.0 <ID> <URL>`
    
    * 通过Iexec market 购买运行

* 

      





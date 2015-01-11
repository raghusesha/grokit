![Alt text](grokit.jpg?raw=true "grokit")

grokit is a developer's tool to setup one of the best available source code search and cross reference engines, [`Opengrok`](http://opengrok.github.io/OpenGrok/).
This repository contains the source code (without external dependencies) for grokit.  If you want to simply download and use grokit with all its dependencies, please visit [`grokit webpage`](http://grokit.pythonanywhere.com)

Dependencies
------------
### Python libraries
- [`bs4`](http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/)
- [`lxml`](https://pypi.python.org/pypi/lxml)

### Tools
- [`Opengrok`](http://opengrok.github.io/OpenGrok/) (ofcourse!)
- [`JRE`](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
- [`exuberant-ctags`](http://ctags.sourceforge.net/)
- [`Apache Tomcat`](http://tomcat.apache.org/)

Usage:
------------
```ruby
# Clone the repository
git clone https://github.com/raghusesha/grokit.git
# Download and copy the dependent tools (check the section above) into the tools directory
cd grokit/tools
# download opengrok. e.g., wget http://java.net/projects/opengrok/downloads/download/opengrok-0.12.1.tar.gz
# download jre, ctags and tomcat
cd ..
python grokit.py --ppath=<path to project source> --action=setup
```
For instant setup and using the tool,
Check the videos: http://www.youtube.com/watch?v=XzrPlAfiC1w and http://www.youtube.com/watch?v=BTGnZShDiqA

Platforms Tested On:
------------
### Linux
- Ubuntu 12.04 64 bit
- Ubuntu 11.04 64 bit

### Windows
- Windows 7 32 bit
- Windows 8 64 bit

Author
------------
Raghu Sesha Iyengar(raghu.sesha@gmail.com, raghu.iyengar@agreeyamobility.net)

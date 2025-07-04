#
# RUN THE INSURER ACP SERVER
#
#  < >

from Ipython.display import IFrame
import os

url = os.environ.get('DLAI_LOCAL_URL').format(port=8888)
IFrame(f"{url}terminals/1", width="800", height="600")
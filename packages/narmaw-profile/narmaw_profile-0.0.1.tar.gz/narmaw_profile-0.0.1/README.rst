(narmaw profile) เป็นตัวอย่างการอัพโหลด package ไปยัง pypi.org
==============================================================

PyPi: https://pypi.org/project/narmaw_profile/

Hello World!!! แพคเกจนี้ไว้สำหรับอธิบายการใช้ OOP และอัพโหลดไปยังเวป
pypi ได้

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install narmaw_profile

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

       my = Profile('Neko')
       my.company = 'narmaw-theseries'
       my.hobby = ['Watch Series', 'Sleeping', 'Cooking']
       print(my.name)
       my.show_email()
       my.show_myart()
       my.show_hobby()
       print('------------------------')
       
       
       friend = Profile('Mumu')
       print(friend.name)
       friend.show_email()

พัฒนาโดย: Mumu Neko 

สอนโดย: ลุงวิศวกร สอนคำนวณ

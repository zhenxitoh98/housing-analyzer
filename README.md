# Housing Analyzer

## Members:
* Samuel Toh
* Mark Wu
* Peggy Zhao

## Data Preparation and Setup
* The database system we are using is Firebase Cloud Firestore. We can use the system by going to this website: https://firebase.google.com/docs/firestore
* All the data is from the Realtor API. You would be able to see the data by running the application.
* To get the data, we first have to perform a read operation to the Realtor API to get the data of the properties in the area. We then perform a write operation to write the data from the API to the database. We perform the script in ***firebase_testing.py*** to read from the API and write to the database.
* We did not benchmark different database systems. we chose to use Firebase Cloud Firestore as the data from the API is already in json format and Firebase Cloud Firestore is a NoSQL database system.
* we did not generate our own data, all data is read from the Realtor API. https://www.realtor.com/

## Application and Code
* The programming languages we are using are Python (Version 3.6), HTML and Javasript.
* There is no thiry-party libraries required but you should install a list of packages first in order to run the code. The list of packages is specified in requirements.txt and is also attached below:
  - APScheduler==3.7.0
  - CacheControl==0.12.6
  - cachetools==4.2.1
  - certifi==2020.12.5
  - cffi==1.14.5
  - chardet==4.0.0
  - click==7.1.2
  - firebase-admin==4.5.3
  - Flask==1.1.2
  - Flask-Caching==1.10.1
  - google-api-core==1.26.3
  - google-api-python-client==2.2.0
  - google-auth==1.29.0
  - google-auth-httplib2==0.1.0
  - google-cloud-core==1.6.0
  - google-cloud-firestore==2.1.0
  - google-cloud-storage==1.37.1
  - google-crc32c==1.1.2
  - google-resumable-media==1.2.0
  - googleapis-common-protos==1.53.0
  - grpcio==1.37.0
  - gunicorn==20.1.0
  - httplib2==0.19.1
  - idna==2.10
  - itsdangerous==1.1.0
  - Jinja2==2.11.3
  - MarkupSafe==1.1.1
  - msgpack==1.0.2
  - packaging==20.9
  - proto-plus==1.18.1
  - protobuf==3.15.8
  - pyasn1==0.4.8
  - pyasn1-modules==0.2.8
  - pycparser==2.20
  - pyparsing==2.4.7
  - pytz==2021.1
  - requests==2.25.1
  - rsa==4.7.2
  - six==1.15.0
  - tzlocal==2.1
  - uritemplate==3.0.1
  - urllib3==1.26.4
  - Werkzeug==1.0.1
* In order to obtain the website, users should first download the packages and then simply run the file **app.py**. A website url will be generated at this moment. Click the link and it will guide users to our search engine.

## Code Documentation and References
* The heapmap utilizes Simplemaps as a templete for Georgia and Alabama map. Statemap-alabama.js and Statemap-georgia.js are generated and added to the project by Simplemaps allowing the Scalable Vector Graphics (SVG) design of the two states.Statemap-alabama.html and Statemap-georgia.html are also downloaded from Simplemaps as a zip file and provide tempelete for Georgia and Alabama maps. 
* data-Alabama.json and data-Georgia.json are added to maintain a record of housing data locally by pulling data from firebase periodically.   
* https://echarts.apache.org/examples/en/index.html

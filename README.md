# T2A2-NBA-Card-Manager-API

## R1 - The problem this app will solve and how it will does this

Sport card collecting, specifically NBA cards, is a very popular hobby within Australia. The hobby broke out into the mainstream during the pandemic where thousands of individuals began to collect and sell various kinds of NBA cards. During this time, listings for cards on auction applications such as EBay and Facebook Marketplace increased by 300%. However, despite this, physical store locations which specalise in sport card collecting have rapidly closed. In Sydney alone, there is no specific physcial store front which sells and is committed to purely sport card sales. This lack of a gathering place has hindered the hobbys growth within Australia as there is no place for individuals who are in invested in this hobby to meet and grow the community to levels it is at in other parts of the world such as America. This can be examplified in the fact that in Australia, over 60% of the individuals who were exposed to the hobby during its heightened popularity in the pandemic have since stepped away.Currently, individuals invested in the hobby must rely on social media applications such as Facebook, Ebay and Instagram to both discuss and potentially sell/trade cards in their collection. This can become a hinderence as from personal experience, managing different lines of communication on multiple different applications can become exhausting, especially for individuals who are looking for specific rare cards. This inconvenience may have attibuted to lesser individuals being invested in the hobby. 

The solution to this is a centralised application which solely designed to serve the various needs of individuals who are invested in NBA card hobby. This API serves as the foundation for this application and provides individuals with a multitude of features to both grow the NBA card collecting communitiy, but also to simplify trading/selling practices within the hobby. It does this by providing three main features. This includes a blogging feature, a feature to display all current cards in an individuals collection, as well as the building blocks to a fully fledged auction house where users can both place their cards on auction and other users can place bids. These features reflect the three core pillars of the card collecting hobby. Having these abilities in a centralised application will propel the hobbies growth in areas where physical meeting is limited and ultimately provide convience to all individuals who are both seasoned card collectors as well as individuals looking to enter the hobby for the first time.

## R3 - Explantion of the third party services, packages and dependencies utilised to create the API

### Main third party services, packages and dependencies utilised 

### Flask

Flask is a web framework designed for Python which allows developers to create and manage web appplications efficiently. It is a WSGI framework, meaning that it acts as a gateway for web servers to pass request to web applications or other frameworks. It relies on the WSGI external library as well as the Jinja2 template engine to operate. It is out of the box, meaning users can install the package straight to Python and automatically begin building frameworks. In this sense, Flask has been utilised as the foundation of the API and handles the routes, requests and responses.

### Flask_JWT_Extended

This is an extension of the Flask framework and is designed to allow JSON Web Token Authentication and Authorization. It does this by creating an instance of these tokens once called upon. These tokens can be utilisied to automatically authenitcate individuals trying to access specific routes within the API.

### Bcrypt

Bcrypt is a library which is designed to increase the security of data which is stored within a RDBMS. It is particularly used to protect passwords and other sensitive information by hashing this information in a which ensures it is securarly stored. It is extremely important to hash all sensitive information, particularly sensitive information provided by clients who utilise the API, to ensure third party breaches do not occur and all client information remains secure.

### SQLAlchemy & Psycopg2

SQLAlchemy is the core package which allows Python to interact with the PostgreSQL database which is connected to the application. This is due to the fact that it is created based upon the object-relational mapping (ORM) principle. Essentially, SQLAlchemy allows developers to query the database in a pythonic manner by treating the models and schemas of the database as Python classess and objects. Building upon this, the tables which are created witin the database are mapped to Python classes, while the rows which are found within those tables are mapped to instances of those classes. In order for SQLAlchemy to effectively interact with the PostgreSQL database, it is necessary to connect the flask application to the database. This is completed by utilising the Psycopg2 library which is designed to facilitate the connection between the database and the Flask application by acting as an adapted between the two.

### Marshmallow

Marshamallow faciliates the exchange of information between the classes and models which are created through SQLAclhemy, to JSON readible data which the API can serve to a client. It does this through three key processes which include serilisation (conversion of objects to native Python data types which can be expressed as JSON), deserialisation (conversion of JSON back to complext Python data types) and validation (ensures the data which is being serliased/deserialised conforms to the rules outlined in the schema which has been created by the developer). Without Marshmallow, it would be extremely difficult/complicated to serve routes with the appropirate data in a JSON format.

### A Complete List of the Dependencies Can be Found Below:

![List of Dependencies](docs/dependencies.png)

## R4 - Benefits and Drawbacks of the API's underlying database system

The database system which has been utilised to for this application includes PostgreSQL. It is a relational database management system which is open source. It is most commonly utilised to build API projects and provides an amptiude of benefits to developers who utilise it in their projects. However, there are some certain drawbacks which inhibit its overally effectivness in certain circumstances.

### Benefits

- **Extensibility:** A major overall benefit of PostgreSQL is it's ability to be highly extensible. Developers have the ability to extend their database they are currently working with which means that if a developer needs to utilise a feature which is not currently supported by PostgreSQL out of the box, the developer can implement and create this feature themselves. This provides a huge amount of flexibility to developers as they can completly finetune all aspects of their database and ensure they are hitting all crucial aspects of their projects. It also ensures that complex requirments which may be imposed by clients have a higher chance of being implemented successfully in a more efficient manner.

- **Open Source:** Another major benefit of PostgreSQL is the fact that it is open source. Open source tools such as PostgreSQL provide a cost effective option for developers as it is completely free to utilise. This factor has lead to PostgreSQL to being utilised in both personal and commercial development settings. The nature of it being open source means that it holds a dedicated base of developers who both maintain and alievate bugs in an efficient manner, but there is a vast community of users who are able to assit individuals who are learning PostgreSQL or who have encounted a blocker while utilising it. This improves effiency in development time for developers at all stages in their development journeys.

- **Security Features:** PostgreSQL has a rich set of security features built into it and these features are designed to to uphold all authorisation of data. There are three key security features at this level which ensure that individuals who do not hold the requisite permissions to access data within the a created database are forbidden from doing so. These include Role-Based Access Control (Allows system admin administrators to manage permissions of users through the use of access roles and grants, which dictate who can access and modify data), Table and Column-Level Permissions (Allow system administrators to give specific table level permissions to restrict who can access schemas of databases) and Row-Level Security (permissions are set to enable access to specific rows within a table).

### Drawbacks

- **Slow Performance:** Unfortunately, when working with large data sets, it is fair to say that PostgreSQL performs relatively slower when compared to other database management systems. This can be attributed to the fact that PostgreSQL is a relational database management system and must read every table in a line by line nature to extract relevent data which may or may not match the query whih is being inputted by the user. This slow standard inhibits PostgreSQL's ability to be utilised in commercial settings where data sets are likely to be huge in nature. It also has the ability to hinder security as backup techniques are more difficult and less efficient to implement. 

- **Complexity:** Due to its advanced features and ability to express many different types of data and relationships, PostgreSQL can be considered to be a complex database to manage. This is specifically true for individuals who are just being exposed to interacting with databases for the first time. As previously stated, there is a huge community who is dedicated to assiting individuals in need of assitance, however, the sheer amount of features that PostgreSQL provides users may be daunting and lead to individuals avoiding utilising the database management system all together.

- **Resource Intensive:** When compared to other databases, PostgreSQL can be considered to be extremely resource intensive and has the ability to bottleneck database performance through overuse of CPU power and memory usage. This is can be extremely prevelent when working with large amounts of data and queries which commonly utilise the * indicator to search the entire regulary. When working with huge data sets, the need for speed is quite important and may lead to developers in investing in more hardware to improve the bottlenecks which are created by PostgreSQL. Depending on the context, this can be quite expensive to maintain.

## R5 - Explaination the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app

The ORM which has been utilised to faciliate the creation of the application is SQLAlchemy. SQLAlchemy allows for the interaction between the database and the Flask application by translating tables and rows in a database to classes and instances in python to ensure seemless integration and communication. In this application, SQLAlchemy is utilised in a multiude of different ways for different purposes. The instance in which it is utilised and the purpose of why it is being used for each circumstance can be found below:

### Creation of database models/instances tables/rows:

#### Designing the databade models/tables

By utilising SQLAlchemy, database tables can be created straight from Python. This is achieved by utilising Python classes to represent each table which is stored in the database. Below is how you would design a class to represent a model of a particular table. In this case, the card model is being displayed: 

![Photo of card model](docs/card_model.png)

In this example, the tables paramaters are being designed the class. The class name is named Card and the paramaters being passed into the class is ```db.model```. This is to examplify to the class that it should have behaviors which are akin to a table in a database. Following on from this, the name in which the table will be called is denoted as a value of the ```__tablename__``` attribute.  In this instance, the table which is based off this model will be called ```'cards'```. 

Following on from this, the attributes of the model are defined. Firstly, the primary key is denoted as the ```id``` attribute which holds the ```primary_key=True``` method to denote that it should be a seriel int type which is unique across all entries in the table. Following on from this, there are 6 other attributes found withiin this table. 

Following on from the attributes, the last two entires in the model are defining the various kinds of relationships this model/table has with other model/tables in the database. In this instance, the model has a one to many relationship with both the ```personal_collections``` and the ```auction``` table in the database. Both these tables utilise the ```id``` attribute of the card models as foregein keys thus solidfying the relationship. 

The purpose of creating these models is to ensure that Flask and the PostgreSQL database are able to effectivly communicate, and there is ease to the developer creating the API to utilise the models of the database as classes in Python to allow easier manipulation in a development sense. 

#### Creation of the tables within the database

SQLAlchemy provides specific ability to create tables in the database straight from Python. The following example shows the syntax for creating tables utilising SQLAlchemy:

![Creation of the tables within the database](docs/table_create.png)

By utilising this syntax, any model which has been imported into the file where this command is being executed will be created within the database with the same structure which has been defined in the creation of the model class.

The ```db.drop_all()``` method will delete all tables from the database which is connected to the Flask app. While the ```db.create_all()``` method will create all tables based on the imported model class connected to the file where this method is being executed.

 Again the purpose of this is to create ease to the developer as well as build upon the ability to create model classes, as this feature would be essentially useless if a developer was not able to actually create the table from the model which has been designed

 #### Creation of rows/instances

 SQLAlchemy provides the ability to create instances of the classes which are created to represent the database model, and treat these instances as rows once they are add the table within the database. An example of the syntax which completes this is found below:

 ![Creation of instances of the model class](docs/rows_create.png)

 As you can see, the ```Card()``` method is called to create an instance of the ```Class Card```. The attributes that are being added to the instance are direct components of those that were created during classes creation. Once the user has finished creating the instance, they will pass the name of the instance to the ```db.session.add_all()``` method. This method will open a session which can be defined as a sort of work space where changes to the database that are pending are held in a waiting area. To effectively add these change to the database, the ```db.session.commit()``` method must be called. This method will close the session and add the changes to the database.

A culmination of the past three code example can be examplified below:

![Card Table](docs/card_table.png)

As you can see, the cards table has been created utilising the class model as the schema for the table. The instances of that class which were created and added to the database are also found and located within the classes table. As such, this processes examplifies how the utilisation of SQLAlchemy has assisted the faciliation of web applications in Flask. 
from typing import Generic , Type,TypeVar
'''
Generic => it lets us create a class that can work with any data type. 
        here we will use it to take mondgodb data and convert/validate it to a pydantic model.

Type => it is used to specify the type of a variable or a function parameter.
TypeVar => it is used to create a type variable teeling i dont konw type yet decide layer  .
        we used it to tell that we dont know which pydantic model it will be but it will be of any base model subclass.
'''

from bson import ObjectId
from pydantic import BaseModel
from loguru import logger
from pymongo import MongoClient,errors
from philoagent.config import settings



T = TypeVar('T', bound=BaseModel)

class MongoDBClientWrapper(Generic[T]):

    def __init__(self,
                 model: Type[T],
                 collection_name: str,
                 database_name: str = settings.MONGO_DB_NAME,
                 mongodb_uri: str = settings.MONGO_URI)->None:
        self.model=model
        self.collection_name=collection_name
        self.database_name=database_name
        self.mongodb_uri=mongodb_uri

        try:
            self.client = MongoClient(mongodb_uri,appname="Philoagent")
            self.client.server_info()  # Trigger a connection to check if it's successful
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
        
        self.database= self.client[self.database_name]
        self.collection=self.database[self.collection_name] 
        logger.info(f"Connected to MongoDB database: {self.database_name}, collection: {self.collection_name}")
    

    def __enter__(self)-> "MongoDBClientWrapper":
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb)-> None:
        self.client.close()
        logger.info("MongoDB connection closed.")

    def clear_collection(self)-> None:
        try:
            result = self.collection.delete_many({})
            logger.info(f"Cleared collection '{self.collection_name}', deleted {result.deleted_count} documents.")
        except errors.PyMongoError as e:
            logger.error(f"Failed to clear collection '{self.collection_name}': {e}")
            raise RuntimeError(f"Failed to clear collection '{self.collection_name}': {e}")
    
    def ingest_documents(self,documents: list[T])-> None:
        try:
            # check all doc are pydantic model instances
            if not documents or not all(isinstance(doc, BaseModel) for doc in documents):
                raise ValueError(f"All documents must be instances of {self.model.__name__}")
            dict_documents =[doc.model_dump() for doc in documents]

            for doc in dict_documents:
                doc.pop("_id", None)
            self.collection.insert_many(dict_documents)
            logger.info(f"Inserted {len(dict_documents)} documents into collection '{self.collection_name}'.")
        except errors.PyMongoError as e:
            logger.error(f"Failed to insert documents into collection '{self.collection_name}': {e}")
            raise RuntimeError(f"Failed to insert documents into collection '{self.collection_name}': {e}")
        

    
            logger.debug("Closed MongoDB connection.")


    def __parse_documents(self, documents: list[dict]) -> list[T]:
        """Convert MongoDB documents to Pydantic model instances.

        Converts MongoDB ObjectId fields to strings and transforms the document structure
        to match the Pydantic model schema.

        Args:
            documents (list[dict]): List of MongoDB documents to parse.

        Returns:
            list[T]: List of validated Pydantic model instances.
        """
        parsed_documents = []
        for doc in documents:
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)

            _id = doc.pop("_id", None)
            doc["id"] = _id

            parsed_doc = self.model.model_validate(doc)
            parsed_documents.append(parsed_doc)

        return parsed_documents

    def get_collection_count(self) -> int:
        """Count the total number of documents in the collection.

        Returns:
            Total number of documents in the collection.

        Raises:
            errors.PyMongoError: If the count operation fails.
        """

        try:
            return self.collection.count_documents({})
        except errors.PyMongoError as e:
            logger.error(f"Error counting documents in MongoDB: {e}")
            raise

    def close(self) -> None:
        """Close the MongoDB connection.

        This method should be called when the service is no longer needed
        to properly release resources, unless using the context manager.
        """

        self.client.close()
        logger.debug("Closed MongoDB connection.")
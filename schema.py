from graphene import ObjectType, String, Schema, Field, List, Interface

import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient()
db = client["starwars"]
humans = db["humans"]
droids = db["droids"]


class Character(Interface):
    _id = String(description="The id of this character.")
    name = String(description="The name of this character.")


class CharacterObject(ObjectType):
    class Meta:
        interfaces = (Character,)


class Droid(ObjectType):
    class Meta:
        interfaces = (Character,)

    function = String(description="The purpose/function of the droid.")
    ownerid = String(description="The id of owner of this droid")


class Human(ObjectType):
    class Meta:
        interfaces = (Character,)

    homePlanet = String(description="The home planet of this human.")
    droids = List(Droid, description="A list of the droids in this human's possesion.")

    def resolve_droids(root, info):
        return db["droids"].find({"ownerid": ObjectId(root["_id"])})[:]


class Query(ObjectType):

    greet = String(name=String(default_value="world"))

    human = Field(
        Human,
        name=String(),
        id=String(),
        description="Find a human by either the name or the id.",
    )

    droid = Field(
        Droid,
        name=String(),
        id=String(),
        description="Find a droid by either the name or the id.",
    )

    def resolve_greet(root, info, name):
        return f"Hello, {name}!"

    def resolve_human(parent, info, name=None, id=None):
        if name:
            return db["humans"].find_one({"name": name})
        if id:
            return db["humans"].find_one({"_id": ObjectId(id)})

    def resolve_droid(parent, info, name=None, id=None):
        if name:
            return db["droids"].find_one({"name": name})
        if id:
            return db["droids"].find_one({"_id": ObjectId(id)})


schema = Schema(query=Query)

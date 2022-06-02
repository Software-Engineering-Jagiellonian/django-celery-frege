# An example of using DataMapper to create database-backed models.
#
# DataMapper is an ORM (Object-Relational-Mapper) that provides a Ruby interface
# to SQL databases.
#
# Website: http://datamapper.org/
#
# This file includes code to:
# - Establish a database connection
# - Define a data model
# - Update the database with the proper schema
# - Seed sample data
#
# Review the comments and code in the file. You can run this file to see some
# example uses of DataMapper.
#
# When you are ready to experiment and explore, open an irb session and require
# this file:
#
# $ irb
# > require "data_mapper.rb"
#
# Once this file has been loaded, you will have access to the `Todo` model and
# can use it to create, read, update, and delete records in the database.
#
# See the DataMapper documentation and "getting started" guide for more
# information.

require "data_mapper" # Require the data_mapper gem
require "sqlite3"     # Require the sqlite adapter for Ruby

# If you want the logs displayed you have to do this before the call to setup
DataMapper::Logger.new($stderr, :debug)

# Establish a connection to an in-memory SQLite database
#
# If you want to use an external database so that your data will persist even
# after this program stops running, you can replace the second argument with a
# string like `sqlite:todo.db`, which would look for a SQLite database file
# called `todo.db` in the current directory
DataMapper.setup(:default, "sqlite::memory:")

# Define a Todo model for keeping track of tasks to complete
#
# DataMapper will attempt to create and use a table called "todos" with the
# columns "id", "task", "complete", and "created_at"
class Todo
  # This is how we get access to all the DataMapper goodness in this class
  include DataMapper::Resource

  # The primary key: an auto-incrementing integer
  property :id, Serial

  # Task is a varchar type string, for short strings (255 chars or fewer)
  property :task, String, required: true

  # Complete is a boolean type property (true or false, false by default)
  property :complete, Boolean, default: false

  # The "created_at" property will default to the current time upon creation
  property :created_at, DateTime, default: proc { DateTime.now }

  # Define our own version of to_s so that Todo items can be converted to
  # human-readable strings
  def to_s
    x_mark = complete ? "X" : " "

    "#{id} - [#{x_mark}] #{task}"
  end
end

# Check all models for validity and initiate all properties with relationships
DataMapper.finalize

# Update the database schema to match the models defined
DataMapper.auto_upgrade!

# This method can be called to insert sample data in the database
def seed_db
  Todo.create(task: "Bake a cake")
  Todo.create(task: "Read Tolstoy")
  Todo.create(task: "Learn FORTRAN")
end

if __FILE__ == $PROGRAM_NAME
  puts ""
  puts "Let's have some fun with DataMapper."

  puts ""
  puts "How many `Todo` records are in the database?"
  puts Todo.count

  puts ""
  puts "Ok, so let's create some. Seeding the database..."
  seed_db

  puts ""
  puts "Now how many are there?"
  puts Todo.count

  puts ""
  puts "Excellent. Let's retrieve all of the records."
  puts Todo.all

  puts ""
  puts "Ok, now let's retrieve the record with id 2."
  puts task = Todo.get(2)

  puts ""
  puts "And then we can mark it as completed."
  task.complete = true
  puts task

  puts ""
  puts "But this didn't actually save the todo to the database, right?"
  puts task.dirty?

  puts ""
  puts "So let's save our changes."
  task.save
  puts task.dirty?

  puts ""
  puts "Now it's your turn! Try creating, updating, and deleting records."
end

# This is a demonstration of Ruby's File.expand_path method.
#
# File.expand_path converts a pathname to an absolute pathname.
#
# Try running this file from a few different locations.
#
# From this directory:
# $ ruby expand_path.rb
#
# From the parent directory:
# $ ruby examples/expand_path.rb
#
# From your home directory
# $ ruby path/to/ruby-examples/examples/expand_path.rb

puts ""
puts "The value of `__FILE__` (the name of this Ruby file) is:"
puts "=> #{__FILE__}"

puts ""
puts "The absolute path of this Ruby file is:"
puts "=> #{File.expand_path(__FILE__)}"

puts ""
puts "The relative path from this file to `args.rb` is:"
puts "=> #{"./args.rb"}"

puts ""
puts "Does `File.exist?` return true for the relative path `./args.rb`?"
puts "=> #{File.exist?("./args.rb")}"

puts ""
puts "The absolute path to `args.rb` is:"
puts "=> #{File.expand_path("../args.rb", __FILE__)}"

puts ""
puts "Does `File.exist?` return true for the absolute path of `args.rb`?"
puts "=> #{File.exist?(File.expand_path("../args.rb", __FILE__))}"

puts ""
puts "The tilde character '~' represents your home directory."
puts "`File.expand_path('~/')` is:"
puts "=> #{File.expand_path('~/')}"

puts ""
puts "A single period '.' represents the current directory."
puts "`File.expand_path('.')` is:"
puts "=> #{File.expand_path('.')}"

puts ""
puts "Two periods '..' represents the parent directory."
puts "`File.expand_path('..')` is:"
puts "=> #{File.expand_path('..')}"

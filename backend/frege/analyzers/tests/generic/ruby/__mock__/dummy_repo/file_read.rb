if ARGV.size == 0
  puts "You didn't tell us what file to read.  Try this command:"
  puts ""
  puts "    ruby file_read.rb random_file.txt"
  exit # This exits the program
end

# If we've reached this line of code, we know the user supplied us with at least
# one command-line argument. We'll assume it's a file for us to read.

file_name = ARGV[0]  # Set the value of file_name to the first command-line argument
file_contents = File.read(file_name) # Read the contents of the file specified by file_name

puts "The contents of #{file_name} are:"
puts "=========="
puts file_contents
puts "=========="

puts ""
puts "The contents of #{file_name} in all upper-case are:"
puts "=========="
puts file_contents.upcase
puts "=========="

puts ""
puts "The contents of #{file_name} in reverse are:"
puts "=========="
puts file_contents.reverse
puts "=========="

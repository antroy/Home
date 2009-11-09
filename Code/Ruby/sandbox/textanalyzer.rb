
lines = 0
words = 0
sents = 0
chars = 0
nonsp = 0
parag = 1

empty = false

File.open('C:\0\text.txt') do |fh|
    while line = fh.gets
        lines += 1
        words += (line.scan(/\s+/).length + 1)
        sents += line.count "."
        chars += line.length
        real_chars = line.split(/\s+/).join.length
        nonsp += real_chars
        if real_chars == 0 and nonsp > 0
            empty = true
        elsif real_chars > 0 and empty
            empty = false
            parag += 1
        end

    end
end

puts "lines #{lines}"
puts "words #{words}"
puts "sents #{sents}"
puts "chars #{chars}"
puts "nonsp #{nonsp}"
puts "parag #{parag}"

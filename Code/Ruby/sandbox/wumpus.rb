# http://www.atariarchives.org/bcc1/showpage.php?page=248

ROOMS = {"a" => ["b","c","r"], "b" => ["a","e","t"], "c" => ["a","d","g"], "d" => ["c","e","f"],
         "e" => ["b","d","j"], "f" => ["d","h","i"], "g" => ["c","h","q"], "h" => ["f","g","k"],
         "i" => ["f","l","j"], "j" => ["e","i","m"], "k" => ["h","l","p"], "l" => ["i","k","n"],
         "m" => ["j","n","t"], "n" => ["l","m","o"], "o" => ["n","p","s"], "p" => ["k","o","q"],
         "q" => ["g","p","r"], "r" => ["a","q","s"], "s" => ["r","o","t"], "t" => ["b","m","s"]}
         
def rand_room
    keys = ROOMS.keys
    keys[rand(keys.length)]
end


class Room
    def initialize(number, content)
        @number = number
        @content = content
        @exits = []
    end

    def describe()
        puts "You're in a room with exits to the following rooms: " 
        rooms = @exits.shuffle
        rooms.each do |room|
            puts room.describe_from_outside
        end

        @exits.each do |room|
            puts "#{room.number})"
        end
    end

    def describe_from_outside
        case @content
        when "bat"
            puts "You hear flapping"
        when "pit"
            puts "You feel a draft"
        end
    end
end

class Me
    def initialize(start)
        @room = start
        @arrows = 5
    end
    
    attr_reader :room

    def room=(room)
        @room = room
    end
end

class Wumpus
    def initialize(room)
        @room = room
    end
    attr_reader :room

    def move
        rooms = ROOMS[@room].clone
        romms.push @room
        @room = rooms[rand(rooms.length)]
    end

    def describe
        "You smell the Wumpus!"
    end
end

class Bat
    def initialize(room)
        @room = room
    end

    attr_reader :room

    def describe
        "You hear flapping"
    end
end

class Pit
    def initialize(room)
        @room = room
    end
    
    attr_reader :room

    def describe
        "You feel a draft"
    end
end


class Game
    def initialize()
        #puts "initializing"
        @me = Me.new "a"
        #puts rand_room
        @wumpus = Wumpus.new(rand_room)
        @bat1 = Bat.new(rand_room)
        @bat2 = Bat.new(rand_room)
        @pit1 = Pit.new(rand_room)
        @pit2 = Pit.new(rand_room)
        @hazards = [ @pit1, @pit2, @wumpus, @bat1, @bat2 ]
    end

    def start
        while true
            enter @me.room
        end
        #@hazards.each do |haz| puts "#{haz}: #{haz.room}" end
    end

    def describe
        puts "This room has exits to rooms #{adjacent_rooms.join(', ')}"

        @hazards.each do |hazard|
            if adjacent_rooms.index(hazard.room)
                puts hazard.describe
            end
        end
    end
    
    def enter(room)
        describe
        puts "What do you want to do now? Move into a room by typing its name. Shoot by typing > followed by a list of up to 5 room names:"
        room = gets.chomp
        @me.room = room
    end

    def adjacent_rooms
        #puts "#{@me.room} adj #{ROOMS[@me.room]}"
        ROOMS[@me.room]
    end

end

game = Game.new
game.start




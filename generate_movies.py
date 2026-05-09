import json

movies_data = [
    ("Inside Out 2", "Animation", "English", "2024", "/vpnVM9B6NMmQpWeZno4Hwj0b0mU.jpg", "LEjhY29DqKw", "Joy, Sadness, Anger, Fear and Disgust are back for a new adventure inside Riley's head."),
    ("Deadpool & Wolverine", "Action", "English", "2024", "/8cdclKEfb26vYmUvI8izSq9pTws.jpg", "uJMCNJP2ipI", "A weary Wolverine finds himself joining forces with a mouthy Deadpool to defeat a common enemy."),
    ("Despicable Me 4", "Animation", "English", "2024", "/wWba3TaoCIBuXNEZ3kyqB6uUmTM.jpg", "qQlbDcqToKk", "Gru and the Minions return for more chaotic fun as they face a new nemesis."),
    ("Kingdom of the Planet of the Apes", "Sci-Fi", "English", "2024", "/gKkl37j96S3uW0PrfsM6hqmRojL.jpg", "XtFI7SNtVpY", "Many years after Caesar's reign, a young ape goes on a journey that will lead him to question everything he's been taught."),
    ("Furiosa: A Mad Max Saga", "Action", "English", "2024", "/iB2jadjolvSoZpY9p3SwwS9pSww.jpg", "XJMuhwVlca4", "The origin story of renegade warrior Furiosa before her encounter with Mad Max."),
    ("Bad Boys: Ride or Die", "Action", "English", "2024", "/nP6RPhSAs3dbSSet9vYnZ9pSww.jpg", "hRFY_Fm-VNM", "Miami's finest are back on the run in this high-octane action comedy."),
    ("The Fall Guy", "Action", "English", "2024", "/t9i0X0X0X0X0X0X0X0X0X0X0.jpg", "j7jPnwVGzgQ", "A stuntman must track down a missing movie star, solve a conspiracy and try to win back the love of his life."),
    ("A Quiet Place: Day One", "Horror", "English", "2024", "/q9o9o9o9o9o9o9o9o9o9o9o.jpg", "YPY7J-flzE8", "Experience the day the world went quiet in this terrifying origin story."),
    ("Civil War", "Action", "English", "2024", "/c9o9o9o9o9o9o9o9o9o9o9o.jpg", "aDyQxtg0V2w", "A journey across a dystopian future America, following a team of military-embedded journalists."),
    ("Challengers", "Drama", "English", "2024", "/ch9o9o9o9o9o9o9o9o9o9o9o.jpg", "VobTTbg-XOk", "Tashi, a tennis player turned coach, has taken her husband, Art, and transformed him from a mediocre player into a world-famous grand slam champion."),
    ("Monkey Man", "Action", "English", "2024", "/m9o9o9o9o9o9o9o9o9o9o9o.jpg", "g8zxiB5Q6sc", "An anonymous young man unleashes a campaign of vengeance against the corrupt leaders who murdered his mother."),
    ("Twisters", "Action", "English", "2024", "/tw9o9o9o9o9o9o9o9o9o9o9o.jpg", "JbS_E0MIdH8", "An update to the 1996 film 'Twister', following a new generation of storm chasers."),
    ("Trap", "Thriller", "English", "2024", "/tr9o9o9o9o9o9o9o9o9o9o9o.jpg", "h3R_7y_845c", "A father and teen daughter attend a pop concert, where they realize they’re at the center of a dark and sinister event."),
    ("Longlegs", "Horror", "English", "2024", "/l9o9o9o9o9o9o9o9o9o9o9o.jpg", "VobTTbg-XOk", "FBI Agent Lee Harker is assigned to an unsolved serial killer case that takes an unexpected turn, revealing evidence of the occult."),
    ("Animal", "Action", "Hindi", "2023", "/an9o9o9o9o9o9o9o9o9o9o9o.jpg", "Dydmpau61I4", "A son's intense love for his father. Often away due to work, the father is unable to comprehend the intensity of his son's love."),
    ("Dunki", "Comedy", "Hindi", "2023", "/du9o9o9o9o9o9o9o9o9o9o9o.jpg", "vN7pGdf_6W0", "Four friends from a village in Punjab share a common dream: to go to England. Their problem is that they have neither the visa nor the ticket."),
    ("Salaar: Part 1 – Ceasefire", "Action", "Telugu", "2023", "/sa9o9o9o9o9o9o9o9o9o9o9o.jpg", "4GPvYMk9WAA", "A gang leader tries to keep a promise made to his dying friend and joins forces with him to take on other criminal gangs."),
    ("Tiger 3", "Action", "Hindi", "2023", "/ti9o9o9o9o9o9o9o9o9o9o9o.jpg", "vqu4z34wENw", "Following the events of Tiger Zinda Hai, War, and Pathaan, Tiger and Zoya are framed as traitors by a revenge-seeking terrorist."),
    ("Rocky Aur Rani Kii Prem Kahaani", "Romance", "Hindi", "2023", "/ro9o9o9o9o9o9o9o9o9o9o9o.jpg", "6mdxyrs_yY0", "A flamboyant Punjabi man and an intellectual Bengali journalist fall in love despite their differences."),
    ("OMG 2", "Drama", "Hindi", "2023", "/om9o9o9o9o9o9o9o9o9o9o9o.jpg", "X-p3S9S9S9y", "An unhappy civilian asks the court to mandate sex education in schools in this spiritual sequel to OMG – Oh My God!"),
    ("Gadar 2", "Action", "Hindi", "2023", "/ga9o9o9o9o9o9o9o9o9o9o9o.jpg", "vhwr4z34wENw", "During the Indo-Pakistani War of 1971, Tara Singh returns to Pakistan to bring back his son, Charanjeet."),
    ("Fighter", "Action", "Hindi", "2024", "/fi9o9o9o9o9o9o9o9o9o9o9o.jpg", "6amkyrs_yY0", "Top IAF aviators come together in the face of imminent danger to form Air Dragons."),
    ("Merry Christmas", "Thriller", "Hindi", "2024", "/me9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Two strangers meet on Christmas Eve. A night of romance turns into a nightmare."),
    ("Hanu-Man", "Action", "Telugu", "2024", "/ha9o9o9o9o9o9o9o9o9o9o9o.jpg", "O3jStuUKWA", "An imaginary place called Anjanadri where the protagonist gets the powers of Hanuman and fights for Anjanadri."),
    ("Premalu", "Romance", "Malayalam", "2024", "/pr9o9o9o9o9o9o9o9o9o9o9o.jpg", "jU3d1sN1Y0c", "Sachin pursues romance with two characters, but his attempts lead to hilarious situations."),
    ("Bramayugam", "Horror", "Malayalam", "2024", "/br9o9o9o9o9o9o9o9o9o9o9o.jpg", "jU3d1sN1Y0c", "A folkloric horror tale set in the dark ages of Kerala."),
    ("Aavesham", "Action", "Malayalam", "2024", "/aa9o9o9o9o9o9o9o9o9o9o9o.jpg", "jU3d1sN1Y0c", "Three teenagers arrive in Bangalore for their engineering education and get involved in a fight with seniors."),
    ("The Goat Life", "Drama", "Malayalam", "2024", "/gl9o9o9o9o9o9o9o9o9o9o9o.jpg", "jU3d1sN1Y0c", "The real-life story of Najeeb, an Indian migrant worker who goes to Saudi Arabia to earn money but finds himself living a slave-like existence herding goats in the middle of the desert."),
    ("Captain Miller", "Action", "Tamil", "2024", "/ca9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A renegade Captain and his unconventional outlaw unit perform daring Heists."),
    ("Ayalaan", "Sci-Fi", "Tamil", "2024", "/ay9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A lost alien seeks help from a human to go back to his home planet while a greedy businessman tries to capture it."),
    ("Blue Star", "Sports", "Tamil", "2024", "/bl9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Two rival cricket teams in Arakkonam face off against each other."),
    ("Lal Salaam", "Drama", "Tamil", "2024", "/la9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A cricket-based film that addresses religious harmony and communal peace."),
    ("Siren", "Thriller", "Tamil", "2024", "/si9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "An ambulance driver becomes a criminal and waits for 14 years to come out of jail to take revenge."),
    ("Exhuma", "Horror", "Korean", "2024", "/ex9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "The process of excavating a sinister grave unleashes dreadful consequences buried underneath."),
    ("Past Lives", "Romance", "Korean", "2023", "/pa9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Nora and Hae Sung, two deeply connected childhood friends, are wrested apart after Nora's family emigrates from South Korea."),
    ("Decision to Leave", "Thriller", "Korean", "2022", "/de9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A detective investigating a man's death in the mountains meets the dead man's mysterious wife in the course of his dogged sleuthing."),
    ("Killers of the Flower Moon", "Crime", "English", "2023", "/ki9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Members of the Osage tribe in northeastern Oklahoma are murdered under mysterious circumstances in the 1920s."),
    ("Napoleon", "History", "English", "2023", "/na9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "An epic that details the checkered rise and fall of French Emperor Napoleon Bonaparte and his relentless journey to power."),
    ("The Killer", "Thriller", "English", "2023", "/tk9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "After a fateful near-miss, an assassin battles his employers, and himself, on an international manhunt he insists isn't personal."),
    ("Wonka", "Fantasy", "English", "2023", "/wo9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "The story of how a young Willy Wonka, full of ideas and determined to change the world one delectable bite at a time."),
    ("Aquaman and the Lost Kingdom", "Action", "English", "2023", "/aq9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Black Manta seeks revenge on Aquaman for his father's death. Wielding the power of the mythic Black Trident, he becomes a formidable foe."),
    ("Ferrari", "Biography", "English", "2023", "/fe9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Set during the summer of 1957, ex-racecar driver Enzo Ferrari is in crisis. Bankruptcy stalks the company he and his wife built."),
    ("The Iron Claw", "Biography", "English", "2023", "/ic9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "The true story of the inseparable Von Erich brothers, who made history in the intensely competitive world of professional wrestling in the early 1980s."),
    ("Poor Things", "Comedy", "English", "2023", "/pt9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "The incredible tale and fantastical evolution of Bella Baxter, a young woman brought back to life by the brilliant and unorthodox scientist."),
    ("The Holdovers", "Drama", "English", "2023", "/ho9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A cranky history teacher at a remote prep school is forced to remain on campus over the holidays with a troubled student."),
    ("May December", "Drama", "English", "2023", "/md9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Twenty years after their notorious tabloid romance gripped the nation, a married couple buckles under the pressure when an actress arrives to do research for a film."),
    ("Maestro", "Biography", "English", "2023", "/ma9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A towering and fearless love story chronicling the lifelong relationship between Leonard Bernstein and Felicia Montealegre Cohn Bernstein."),
    ("Priscilla", "Biography", "English", "2023", "/pr9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "When teenage Priscilla Beaulieu meets Elvis Presley at a party, the man who is already a meteoric rock-and-roll superstar becomes someone entirely unexpected."),
    ("Saltburn", "Thriller", "English", "2023", "/sa9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "A student at Oxford University finds himself drawn into the world of a charming and aristocratic classmate, who invites him to his eccentric family's sprawling estate."),
    ("The Creator", "Sci-Fi", "English", "2023", "/tc9o9o9o9o9o9o9o9o9o9o9o.jpg", "Po3jStuUKWA", "Amid a future war between the human race and the forces of artificial intelligence, a hardened ex-special forces agent is recruited to hunt down and kill the Creator.")
]

start_id = 26
new_movies = []
for i, m in enumerate(movies_data):
    new_movies.append({
        "id": start_id + i,
        "title": m[0],
        "genre": m[1],
        "lang": m[2],
        "year": m[3],
        "img": f"https://image.tmdb.org/t/p/w500{m[4]}",
        "video": f"https://www.youtube.com/embed/{m[5]}",
        "description": m[6]
    })

print(json.dumps(new_movies, indent=4))

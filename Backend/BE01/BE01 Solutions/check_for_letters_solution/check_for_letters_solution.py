fin = open("words.txt", "r")
fout = open("letters.txt", "w")

letters = input("Enter a three-letter sequence >> ")

for line in fin:
  word = line.strip()

  pos0 = word.find(letters[0])
  if pos0 > -1:
    pos1 = word.find(letters[1], pos0 +1)
    if pos1 > -1:
      pos2 = word.find(letters[2], pos1 + 1)
      if pos2 > -1:
        fout.write(word + '\n')
        print(word)

fin.close()
fout.close()


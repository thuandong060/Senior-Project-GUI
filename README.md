# Senior-Project-GUI
 Available on Tuesday, January 7, 2020 12:47 PM EST
Develop a chess playing application, with a GUI that displays the board and allows the human player to move according to the rules of the game.   You do not need to be a chess player to work on this project, chess familiarity is not required.

A chess variant will be the goal (attached file) which adds some new features and capabilities to standard chess rules.

Sponsor/Contact: Dr. Hoganson

You may write your application in Java or any other language/platform that produces a sharable game executable.

Clearly there are multiple aspects to this project:  understanding the variant; developing a GUI to play the game;  developing an AI system to play against a human opponent.

For the AI, you will use a distributed AI model!   The "armies" of chess pieces for the AI is divided into three "corp":

The "left" side bishop commands the three left pawns and the left knight.
The "right" side bishop commands the three right pawns and the right bishop
The king commands the queen, two rooks, and the remaining two center pawns (the king may delegate any of its pieces to be commanded by either bishop, at any time, based on your AI decision process.
Pieces scan their local areas for opportunities or threats, and provide the results of their observations to their commander (bishop or king).   The commander (bishop or king) makes decisions based on the input from the the pieces it commands, and may also do its own scan of the board, and makes decision on the actions of its pieces (move or attack, the knight and queen make both move and attack).  The bishops may move themselves and engage in combat.

Start small, get your communication between pieces working.  Then as time allows add more sophisticated planning ideas over two or more turns, and add identifying threats and possible responses.  The AI system will need to scan the board looking for situations where the tactical rules will come into play.

For instance: scan the board to look for situations where the computer's more powerful piece can attack a less powerful enemy piece - where there is an advantage in the probability of a successful attack (the fuzzy logic).

Another example idea:  scan the board to look for situations where the computer's pieces may be vulnerable to an attack by the human component, and look for a piece to move to adjacent to the vulnerable piece, in order to make a subsequent attack on the human player's piece.  

Extra credit if you share a common turn play communication protocol, to allow two AIs to play against each other.

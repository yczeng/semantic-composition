# semantic-compositions

### Explanation
Newly encountered words are generated a random, binary vector containing $-1s$ and $1s$ (using $-1$ and $1$ lets us use the multiplication operator for xor) that is stored as an environment vector $e_i$. Each newly generated word additionally is given a memory vector $m_i$ that is the linear combination of the environment vectors of surrounding words multiplied by their part of speech $s_i$ and their structural relationship $r_i$ (each of which is also symbolically represented by a $d$ dimensional random, binary vector of $-1s$ and $1s$).

The structural relationship $r_i$ is encoded as the movements needed to move from one word to another on the parse tree hierarchically. For example, the movement required to move from one leaf node to an adjacent leaf node when they have the same parent would be "up, down", which would be encoded as "10". Similarly, if moving from one word to another requires moving up the tree twice and then moving down three times, then the movement would be encoded as "11000". These movements are symbolically represented by $d$ dimensional random, binary vectors consisting of $-1s$ and $1s$.

For more information, see the poster [here](CULC13_Poster.pdf)

### Running the program

To use, run `main.py`. This is currently running parse trees from [1000 sentences from the British National Corpus database](http://nclt.computing.dcu.ie/~jfoster/resources/bnc1000.html).

The program will prompt you to input concept1, idea1, concept2, and number of results respectively. These represent m_1, s_2, and m_2 respectively where the analogy you want to find from the data is "m_1 is to s_2 as m_2 is to what?"

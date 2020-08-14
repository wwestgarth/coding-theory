# coding-theory
Crude implementation of results from Coding and Information Theory

https://en.wikipedia.org/wiki/Hamming_code

The idea is that given a set of objects a particular encoding can be chosen that when concatenated into a bit-stream and sent through a lossy channel, any 
flipped bits can be indentified or even recovered.


## Example

We choose a basis of objects and a hamming distance, and a Coding for those elements is chosen

        cipher = code.Code(["a", "b", "c", "d"], hamming_distance=5)

An arbitrary list of elements from this basis can then be encoded into a bit-stream

        cipher.encode(["a", "a", "c", "d"]) -> '0000000000000000000011111000001111111111'

If this stream were to be transmitted through a lossy channel and bits become flipped, with a sufficiently large hamming-distance the errors can be detected

        cipher.decode('0000010000000000000011111000001110111111') -> [None, 'a', 'c', None]

These errors can then be attempted to be recovered, the accuracy of which is dependent on the size of the hamming distance and the serverity of the loss

        cipher.set_attempt_recovery(True)
        cipher.decode('0000010000000000000011111000001110111111') -> ['a', 'a', 'c', 'd']
        
 ## Caveat
 The Coding implemented here is crude and not optimised, it was simply thrown together to see it in practise. There is a trade off between the length of the encoded 
 stream and the hamming distance -- increasing the hamming distance will increase the length of the encoded stream, but a longer stream increases the probability of 
 a flipped bit along a lossy channel. The problem, infact, reduces to an n-dimension sphere packing problem. The hamming-distance represents the radius of the 
 n-Spheres, and the requirement is that they are packed as closely as possible to reduce the information necessary to represent the position of the sphere.
 
 For more information on tightly packed codings, see Golay Code or Hamming(7,4).

import numpy as np

a = np.random.choice([-1, 1], size=10000)
b = np.random.choice([-1, 1], size=10000)
c = np.random.choice([-1, 1], size=10000)
d = np.random.choice([-1, 1], size=10000)
e = np.random.choice([-1, 1], size=10000)
f = np.random.choice([-1, 1], size=10000)


perm1 = np.random.choice([-1, 1], size=10000)
perm2 = np.random.choice([-1, 1], size=10000)
perm3 = np.random.choice([-1, 1], size=10000)
perm4 = np.random.choice([-1, 1], size=10000)


def p1(letter):
	return(np.concatenate([letter[1:], letter[:1]]))

def p2(letter):
	return(np.concatenate([letter[2:], letter[:2]]))

def p3(letter):
	return(np.concatenate([letter[7:], letter[:7]]))

def p4(letter):
	return(np.concatenate([letter[56:], letter[:56]]))

def p2_1(letter):
	return(np.concatenate([letter[-58:], letter[:-58]]))

result = p1(p3(a) + p4(b)) + p2(p3(c) + p4(d))
# equivalent to p13(a) + p14(b) + p23(c) + p24(d)

result2 = p1(p3(a) + p4(e)) + p2(p3(f) + p4(d))
# equivalent to p13(a) + p14(e) + p23(f) + p24(d)

result3 = p1(p3(a) + p4(b)) + p2(p3(f) + p4(d))
# equivalent to p13(a) + p14(e) + p23(f) + p24(d)

result4 = p1(p3(b) + p4(a)) + p2(p3(e) + p4(f))
# equivalent to p13(a) + p14(e) + p23(f) + p24(d)

result5 = perm1*(perm3*a + perm4*b) + perm2*(perm3*c + perm4*d)

result6 = perm1*(perm3*a + perm4*e) + perm2*(perm3*c + perm4*d)

result7 = perm1*a + perm4*b + perm2*(perm3*c + perm4*d)

# print([np.dot( p2_1(result), letter ) for letter in [a, b, c, d, e]])

# print(np.dot(result, result3))
# print(np.dot(result, result2))
# print(np.dot(result, result4))

# print([np.dot( p1(p3(a) + p4(b)) + , letter ) for letter in [a, b, c, d, e]])

print([np.dot( result5 * result6 * b, letter ) for letter in [a, b, c, d, e]])

print(np.dot(result5, result6))
print(np.dot(result5, result7))
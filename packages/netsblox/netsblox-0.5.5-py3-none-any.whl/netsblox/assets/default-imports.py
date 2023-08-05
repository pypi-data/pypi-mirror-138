[
    ['time', 'time', '''
        The `time` package brings in several utilities related to measuring time.

        Here is a list of especially useful functions:
         - `time.sleep(t)` lets your scripts wait a certain number of seconds before resuming.
         - `time.time()` gives you the current timestamp. You can subtract two times to get the time interval in seconds.
    '''],
    ['math', 'math', '''
        The `math` module brings in many common mathematical functions such as `sin`, `cos`, `tan`,
        inverse trig, exponentiation, and many more specialized tools.

        This is useful if you need to compute a handful of operations in your scripts.
        However, if you need to do a lot of number crunching, consider using the `numpy` package instead.
    '''],
    ['random', 'random', '''
        The `random` module allows you to generate random numbers.

        Here is a list of especially useful functions:
         - `random.random()` gives you a float (decimal) number between 0.0 and 1.0 (not including 1.0).
         - `random.randrange(a,b)` gives you a random integer in `range(a,b)`.
        Just like the `range` function, you can pass a single argument to default the first to 0.
    '''],
    ['fractions', 'frac', '''
        The `fractions` module (`frac` for short) allows you to do math directly on rational numbers (fractions).

        If you use built-in types like `float` to do numeric calculations, you might encounter some amount of rounding error.
        This is because `float` has a maximum number of "significant digits" it can represent, meaning it cannot store all numbers exactly.
        For instance, the number `1/3` written in binary has an infinite repeating patterns of 1's and 0's, so `float` cannot store it exactly.
        On the other hand, `frac.Fraction` stores the number as a pair of integers (numerator and denominator), so fractions can be stored exactly.

        To create a fraction, you can use `frac.Fraction(my_number)` to perform the conversion.
        Fractions support the typical math operators, so you can write (frac.Fraction(773) / frac.Fraction(3))**2 and it will give you
        back a fraction containing exactly 597529/9 (the same calculation using `float` has an error of `1.4552e-11`).
        Although rounding error from individual operations on `float` are small, they add up when performing many calculations.
        `frac.Fraction` can be used to avoid any error, so long as you only use operations that work with rational numbers
        (e.g., you cannot take the cos of a fraction, but you can add, subtract, multiply, divide, raise to integer powers, etc.).

        Printing out a fraction will show the value in fraction form.
        If you want to convert the fraction into a `float` (e.g., to display it as a decimal),
        you can use `float(my_frac)` to perform the conversion.
    '''],
    ['numpy', 'np', '''
        The `numpy` package is a highly specialized tool for doing a lot of number crunching very very quickly.
        By convention, `numpy` is typically imported as `np` for brevity.

        Most `numpy` functions work on arrays (lists). To make a `numpy` array, simply use `np.array(some_list)`.
        `numpy` arrays perform their operations in batches.
        For instance, if you have two `numpy` arrays `p` and `q`, each of which is an array of three numbers like 3D coordinates,
        you can simply write `p+q` and numpy will add the components together and give you a new array.
        Many operations are supported, for instance `np.sin(p + 2 * q**2)` will square all the elements of `q`, double them,
        add them to the elements of `p`, then take the `sin` of each element and give the result as a new array.

        `numpy` arrays are actually multi-dimensional arrays.
        A 1D array is a "normal" array (list).
        A 2D array is a matrix.
        In higher dimensions (and in general) these are called tensors, and are commonly used in advanced applications like machine learning.
        If you pass `np.array()` a list of lists, you will get an N-dimensional array (tensor) with the same structure.

        Python supports list slicing. For instance `p[3:5]` gets the sublist of elements with index 3 up to (but not including) 5.
        However, python lists do not support higher-dimensional slicing (even if they are lists of lists).
        But `numpy` arrays allow this, with each dimension separated by a comma.
        For instance if `p` is a 5x5 matrix, `p[1,2:4]` gives row index 1 elements 2 up to 4, and `p[1:-1,1:-1]` gives you the 3x3 matrix in the middle.

        As you can see, `numpy` lets you do a lot of work very quickly and without much typing.
    '''],
]
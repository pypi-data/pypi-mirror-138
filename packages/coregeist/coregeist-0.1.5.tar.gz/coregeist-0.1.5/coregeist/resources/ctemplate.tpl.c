#include <stdlib.h>
#include <stdio.h>
#include "geisten.h"

//Platform specific function definitions
void binarize_i(
        size_t len, const int input[len], int bias[len],
        $binary_type binArray[len / NBITS($binary_type) + 1]) {
    foreach_to(i, len)
    {
        binArray[WORDS_INDEX(binArray, i)] = binarize(binArray[WORDS_INDEX(binArray, i)], WORDS_POS(binArray, i),
                                                      bias[i], input[i]);
    }
}

void binarize_u8(
        size_t len, const uint8_t input[len], int bias[len],
        $binary_type binArray[len / NBITS($binary_type) + 1]) {
    foreach_to(i, len)
    {
        binArray[WORDS_INDEX(binArray, i)] = binarize(binArray[WORDS_INDEX(binArray, i)], WORDS_POS(binArray, i),
                                                      bias[i], input[i]);
    }
}

void binarize_scaled_i(
        size_t len, const int input[len], int scale, int bias[len],
        $binary_type binArray[len / NBITS($binary_type) + 1]) {
    foreach_to(i, len)
    {
        binArray[WORDS_INDEX(binArray, i)] = binarize(binArray[WORDS_INDEX(binArray, i)], WORDS_POS(binArray, i),
                                                      bias[i], input[i] * scale);
    }
}

void binarize_scaled_u8(
        size_t len, const uint8_t input[len], int scale, int bias[len],
        $binary_type binArray[len / NBITS($binary_type) + 1]) {
    foreach_to(i, len)
    {
        binArray[WORDS_INDEX(binArray, i)] = binarize(binArray[WORDS_INDEX(binArray, i)], WORDS_POS(binArray, i),
                                                      bias[i], input[i] * scale);
    }
}

#define binarize_activation(_len, _input, _bias, _binArray) _Generic((_input), \
                    uint8_t *: binarize_u8, \
                        int *: binarize_i  \
              )((_len), (_input), (_bias), (_binArray))

#define binarize_scaled_activation(_len, _input, _scale, _bias, _binArray) _Generic((_input), \
                    uint8_t *: binarize_scaled_u8, \
                        int *: binarize_scaled_i  \
              )((_len), (_input), (_scale), (_bias), (_binArray))

void linear2d(
        size_t m, size_t n,
        const $binary_type weights[n][m / NBITS($binary_type) + 1],
        const $binary_type layer_in[m / NBITS($binary_type) + 1],
        int layer_out[n]) {
    foreach_to(j, n)
    {
        layer_out[j] = 0;
        foreach_to(i, (m / NBITS($binary_type) + 1))
        {
            layer_out[j] += linear(weights[j][i], layer_in[i]);
        }
    }
}

int prelu(int x, int bias, int resolution){
    return (x > 0) * x + ((x < 0) * x * bias) / resolution;
}

void prelu2d(size_t m, const int layer_in[m], int resolution, const int bias[m], int layer_out[m]) {
    foreach_to(i, m)
    { layer_out[i] = prelu(layer_in[i], bias[i], resolution); }
}

void scale(size_t m, const int layer_in[m], int scaling_factor, int layer_out[m], int resolution) {
    foreach_to(i, m)
    { layer_out[i] = (layer_in[i] * scaling_factor) / resolution; }
}

/**
 * argmax() - Returns the index with the largest value across the array.
 * - 'm' The length of the array
 * - 'layer_in' The input array
 *
 * In the case of identity, it returns the smallest index.
 * Returns the index with the largest value
 */
size_t argmax(size_t m, const int layer_in[m]) {
    size_t max_index = 0;
    int max = INT_MIN;
    foreach_to(i, m)
    {
        if (layer_in[i] > max) {
            max = layer_in[i];
            max_index = i;
        }
    }
    return max_index;
}


//define the weights and parameters

$declaration

int main(void) {

    // attempt to read the array of type $input_type and store 
    // the value in the "input" array 
    while (fread($input_name, sizeof($input_type), $input_size, stdin) == $input_size) {
        $layers
        printf("%d\n", $output_value[0]);
    }
    return EXIT_SUCCESS;
}
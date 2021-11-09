#include <stdexcept>
#include "GostCipher.h"

/*
Thanks to Arthur Mamedov for this algorithm!
*/

inline void GostCipher::_64bits_block_to_2_32bit_blocks(const uint8_t block[8], uint32_t& N1, uint32_t& N2) {
	for (int c = 0; c < 4; c++) {
		N1 = (N1 << 8) | block[c];
		N2 = (N2 << 8) | block[c + 4];
	}
}

inline void GostCipher::_2_32bits_blocks_to_64_block(uint32_t N1, uint32_t N2, uint8_t block[8]) {
	for (int c = 3; c >= 0; c--) {
		block[c + 4] = static_cast<uint8_t>(N1);
		block[c] = static_cast<uint8_t>(N2);
		N1 = N1 >> 8;
		N2 = N2 >> 8;
	}
}

void GostCipher::encrypt(uint8_t* block) {
	uint32_t N1, N2;

	_64bits_block_to_2_32bit_blocks(block, N1, N2);

	for (uint8_t c = 0; c < 24; c++) {
		_round(&N1, &N2, c);
	}

	for (uint8_t c = 31; c >= 24; c--) {
		_round(&N1, &N2, c);
	}

	_2_32bits_blocks_to_64_block(N1, N2, block);
}

void GostCipher::decrypt(uint8_t* block) {
	uint32_t N1, N2;

	_64bits_block_to_2_32bit_blocks(block, N1, N2);

	for (uint8_t c = 0; c < 8; c++) {
		_round(&N1, &N2, c);
	}

	for (uint8_t c = 31; c >= 8; c--) {
		_round(&N1, &N2, c);
	}

	_2_32bits_blocks_to_64_block(N1, N2, block);
}

inline void GostCipher::_round(uint32_t* block32b_1, uint32_t* block32b_2, uint8_t i) {
	uint32_t rnd, temp;

	rnd = (*block32b_1 + _round_keys[i % 8]);

	rnd = _substitution_table(rnd, i % 8);

	rnd = (rnd << 11) | (rnd >> 21);

	temp = *block32b_1;
	*block32b_1 = rnd ^ *block32b_2;
	*block32b_2 = temp;
}

inline uint32_t GostCipher::_substitution_table(uint32_t block32b, uint8_t sbox_row) {
	uint8_t blocks4bits[4];
	_split_32bits_to_8bits(block32b, blocks4bits);
	_substitution_table_by_4bits(blocks4bits, sbox_row);
	return _join_4bits_to_32bits(blocks4bits);
}

inline void GostCipher::_substitution_table_by_4bits(uint8_t* blocks4b, uint8_t sbox_row) {
	uint8_t block4b_1, block4b_2;
	for (uint8_t i = 0; i < 4; ++i) {
		block4b_1 = _sbox[sbox_row][blocks4b[i] & 0x0F];
		block4b_2 = _sbox[sbox_row][blocks4b[i] >> 4];
		blocks4b[i] = block4b_2;
		blocks4b[i] = (blocks4b[i] << 4) | block4b_1;
	}
}

inline void GostCipher::_split_256bits_to_32bits(const char* key256b) {
	size_t inc = 0;
	for (uint32_t* p32 = _round_keys; p32 < _round_keys + 8; ++p32) {
		for (uint8_t i = 0; i < 4; ++i)
			*p32 = (*p32 << 8) | (key256b[i + inc]);
		inc += 4;
	}
}

inline void GostCipher::_split_32bits_to_8bits(uint32_t block32b, uint8_t* blocks8b) {
	for (uint8_t i = 0; i < 4; ++i) {
		blocks8b[i] = (uint8_t)(block32b >> (24 - (i * 8)));
	}
}

inline uint32_t GostCipher::_join_4bits_to_32bits(uint8_t* blocks4b) {
	uint32_t block32b = 0;
	for (uint8_t i = 0; i < 4; ++i) {
		block32b = (block32b << 8) | blocks4b[i];
	}
	return block32b;
}

GostCipher::GostCipher(const char* key) {
	if (strlen(key) != 32) {
		throw std::runtime_error("Key length for GOST28147-89 must be 32 bytes long.");
	}
	_split_256bits_to_32bits(key);
}

GostCipher::GostCipher(const GostCipher& gost) {
	for (size_t c = 0; c < 8; c++) {
		_round_keys[c] = gost._round_keys[c];
		for (size_t p = 0; p < 16; p++) {
			_sbox[c][p] = gost._sbox[c][p];
		}
	}
}

void GostCipher::set_key(const char* key) {
	if (strlen(key) != 32) {
		throw std::runtime_error("Key length for GOST28147-89 must be 32 bytes long.");
	}
	_split_256bits_to_32bits(key);
}

void GostCipher::set_substitution_tables(const uint8_t** sbox, const uint8_t** inv_sbox) {
	UNREFERENCED_PARAMETER(inv_sbox);
	for (size_t c = 0; c < 8; c++) {
		for (size_t p = 0; p < 16; p++) {
			_sbox[c][p] = sbox[c][p];
		}
	}
}

size_t GostCipher::get_block_length() const noexcept {
	return 8;
}
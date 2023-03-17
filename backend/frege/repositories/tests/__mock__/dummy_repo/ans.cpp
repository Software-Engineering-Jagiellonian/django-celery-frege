#include"ans.h"

inline double ANS::bits_needed(std::size_t length)
{
	return log2(length);
}

std::vector<char> ANS::encode(const std::string& file_name)
{
	create_alphavite();
	//spread();
	calculate_k();
	calculate_nb();
	create_states_table();
	create_start_table();
	create_encoding_table();
	std::cout << "encoding" << std::endl;
	for (int e : encoding) {
		std::cout << e << " ";
	}
	std::cout << std::endl;
	std::size_t state = 0;
    std::vector<char> all_bits;
	for (char s : data) {
		int number_of_bits = calculate_number_of_bits(state, s);
		std::vector<char> bts = use_bits(state, number_of_bits);
		state = get_next_state_encoder(number_of_bits, state, s) - alphavite_size;
		std::cout << state << std::endl;
		for (char c : bts) {
			all_bits.push_back(c);
		}
	}
	std::cout << "last state: " << state << std::endl;
	std::cout << "bits: " << std::endl;
	std::ofstream out(file_name);
	out << letters.size()<<std::endl;
	for (char c : letters) {
		out << c << " ";
	}
	out << std::endl;
	for (std::size_t i : frequency) {
		out << i << " ";
	}
	out << std::endl;
	out << number_of_states << std::endl;
	out << alphavite_size << std::endl;
	out << state << std::endl;
	out << all_bits.size()<<std::endl;
	for (char c : all_bits) {
		std::cout << c;
		out << c;
	}
	std::cout << std::endl;
	out << std::endl;
	out.close();
	return std::move(all_bits);
};

inline void ANS::create_alphavite()
{
	std::size_t current_sum = frequency[0];
    for (std::size_t i = 0, j = 0; i < alphavite_size; i++) {
		if (i == current_sum) {
			current_sum += frequency[++j];
		}
		alphavite.push_back(letters[j]);
	}
	number_of_states = alphavite_size;
	std::cout << "alphavite " << std::endl;
	for (char c : alphavite) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
};

inline void ANS::spread()
{
	int i = 0;
	int step = (alphavite_size)/8  + 3;

	for (int k = 0; k < letters.size(); k++) {
		for (int j = 0; j < frequency[k]; j++) {
			alphavite[i] = letters[k];
			i = (i + step) % alphavite_size;
		}
	}
	std::cout << "spread " << std::endl;
	for (char c : alphavite) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
}
inline void ANS::calculate_k()
{
	std::size_t R = (std::size_t) bits_needed(alphavite_size);
	k.resize(letters.size(), 0);
	for (std::size_t i = 0; i < letters.size(); i++) {
		k[i] = R - floor(log2(frequency[i]));
	}
	std::cout << "k: " << std::endl;
	for (int c : k) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
}
inline void ANS::calculate_nb()
{
	std::size_t R = (std::size_t) bits_needed(alphavite_size);
	std::size_t r = R + 1;
	nb.resize(letters.size(), 0);
	temp_nb.resize(MAXSIZE, 0);
    for (int i = 0; i < letters.size(); i++) {
		nb[i] = (k[i] << r) - (frequency[i] << k[i]);
		temp_nb[letters[i]] = nb[i];
	}

	std::cout << "nb: " << std::endl;
	for (int c : nb) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
}

inline void ANS::create_states_table()
{
	states.resize(number_of_states, 0);
	for (std::size_t i = 0, j = number_of_states; i < number_of_states; i++) {
		states[i] = j++;
	}
	std::cout << "states: " << std::endl;
	for (int c : states) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
};

inline void ANS::create_start_table()
{
	std::cout << "start: " << std::endl;
	start.resize(MAXSIZE, 0);
	for (std::size_t i = 0; i < frequency.size(); i++) {
		start[letters[i]] = -frequency[i];
		if (i != 0) {
			for (int j = 0; j < i; j++) {
				start[letters[i]] += frequency[j];
			}
			std::cout << start[letters[i]] << " ";
		}
	}
}
inline void ANS::create_encoding_table()
{
	encoding.resize(alphavite_size, 0);
	next = temp_freq;
	std::cout << alphavite_size << std::endl;
	for (std::size_t i = alphavite_size; i < 2 * alphavite_size; i++) {
		char s = alphavite[i - alphavite_size];
		std::cout << "ok" << start[s] + next[s] << std::endl;
		encoding[start[s] + next[s]] = i;
		next[s]++;
	}
}
inline int ANS::calculate_number_of_bits(int state_index, char symbol)
{
	std::size_t R = (std::size_t) bits_needed(alphavite_size);
	std::size_t r = R + 1;
	return (states[state_index] + temp_nb[symbol]) >> r;
};

inline int ANS::get_next_state_encoder(std::size_t number_of_bits, std::size_t state_index, char letter)
{
	int x_tmp = (states[state_index] >> number_of_bits);
	int start_value = start[letter];
	return encoding[start_value + x_tmp];
};

std::vector<char> ANS::use_bits(std::size_t state_index, std::size_t number_of_bits)
{
	int temp = states[state_index];
	std::vector<char> bts;
	for (int i = 0; i < number_of_bits; i++) {
		if (temp % 2 == 1) {
			bts.push_back('1');
		}
		else {
			bts.push_back('0');
		}
		temp = temp >> 1;
	}
	return std::move(bts);
};




ANS::ANS(const std::string& file_name, std::size_t expected_size) {
	std::ifstream in(file_name);
	std::vector<bool> is_present(MAXSIZE, false);
	temp_freq.resize(MAXSIZE, 0);
	if (expected_size) {
		letters.reserve(expected_size);
	}
	alphavite_size = 0;
	char c;
	while (in >> c) {
		std::cout << c << " ";
		data.push_back(c);
		if (!is_present[c]) {
			letters.push_back(c);
			is_present[c] = true;
		}
		temp_freq[c]++;
		alphavite_size++;
	}
	std::cout << std::endl;
	for (char c : letters) {
		frequency.push_back(temp_freq[c]);
	}
	std::cout << "letters" << std::endl;
	for (char c : letters) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
	std::cout << "frequency" << std::endl;
	for (int c :frequency) {
		std::cout << c << " ";
	}
	std::cout << std::endl;
	in.close();
};

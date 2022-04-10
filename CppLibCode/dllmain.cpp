
#define _CRT_SECURE_NO_WARNINGS
#define BUILD_DLL
#include "pch.h"
using namespace std;
extern "C"	{
	struct Word {
		string word;
		int score, i, j, wordInd;
		bool h = false;
		Word() {};
		Word(string word, int i, int j, bool h, int score, int wordInd) :
			word(word), i(i), j(j), h(h), score(score), wordInd(wordInd) {};
	};

	int getMultiplicator(int i, int j) {
		if ((!i && (!j || j == 15 / 2 || j == 14)) ||
			(i == 15 / 2 && (!j || j == 14)) ||
				(i == 14 && (!j || j == 15 / 2 || j == 14))) return 33;
		if ((i == j || i == 15 - j - 1) && abs(i - 15 / 2) >= 3) return 22;
		if (i % 4 == 1 && j % 4 == 1) return 3;
		if ((abs(i - 15 / 2) == 7 && (j % 8 == 3)) ||
			(abs(i - 15 / 2) == 4 && (j % 7 == 0)) || 
			(abs(i - 15 / 2) == 0 && (j % 8 == 3)) || 
			(abs(i - 15 / 2) == 1 && abs(j - 15 / 2) == 1) || 
			(abs(i - 15 / 2) == 5 && abs(j - 15 / 2) == 1) || 
			(abs(i - 15 / 2) == 1 && abs(j - 15 / 2) == 5)) return 2;
		return 1;
	}

	vector<string> dic;
	MY_LIB_EXPORTS void __stdcall loadWords(const char* dictPath) {
		ifstream file(dictPath);
		int cnt = 0;
		while (!file.eof()) {
			string word, meaning;
			getline(file, word);
			dic.push_back(word);
			++cnt;
		}
		cout << "size of dic : " << dic.size() << endl;
	}
	MY_LIB_EXPORTS int __stdcall solve(char** m, 
		const char* l, const char* path, int wordsInSolution) {

		// letters cost map
		map<char, int> cost;
		cost['a'] = 1;
		cost['b'] = 3;
		cost['c'] = 1;
		cost['d'] = 3;
		cost['e'] = 2;
		cost['f'] = 1;
		cost['g'] = 3; // ё
		cost['h'] = 5;
		cost['i'] = 5;
		cost['j'] = 1;
		cost['k'] = 4;
		cost['l'] = 2;
		cost['m'] = 2;
		cost['n'] = 2;
		cost['o'] = 1;
		cost['p'] = 1;
		cost['q'] = 2;
		cost['r'] = 1;
		cost['s'] = 1;
		cost['t'] = 1;
		cost['u'] = 2;
		cost['v'] = 10;
		cost['w'] = 5;
		cost['x'] = 5;
		cost['y'] = 5;
		cost['z'] = 8;
		cost['0'] = 10;
		cost['1'] = 10;
		cost['2'] = 4;
		cost['3'] = 3;
		cost['4'] = 8;
		cost['5'] = 8;
		cost['6'] = 3;
		cost['_'] = 2;
		// player's letters
		string letters(l);
		// game board
		vector<string> matrix(15);
		for (int i = 0; i < 15; ++i) {
			string str(m[i]);
			matrix[i] = str;
			cout << "|" << str << "|" << endl;
		}
		cout << "letters : " << letters << endl;
		cout << "dic size : " << dic.size() << endl;
		int cnt = 0;
		vector<Word> words;
		string filePath = path;
		ofstream f(filePath);
		for (int wordInd = 0; wordInd < dic.size(); ++wordInd) {
			string word = dic[wordInd];
			if (word.size() <= 2) continue;
			// try to put word horizontally
			for (int i = 0; i < 15; ++i) {
				for (int j = 0; j < 15 - word.size() + 1; ++j) {
					bool flag = true; int needSize = 0;
					vector<int> count(256); queue<int> blankedLetters;
					for (char ch : letters) {
						count[ch]++;
					}
					for (int k = j; k < j + word.size(); ++k) {
						if (matrix[i][k] != ' ') {
							if (matrix[i][k] != word[k - j]) {
								flag = false;
								break;
							}
						}
						else {
							char ch = word[k - j];
							if (count[ch] <= 0) {
								if (count['_']) {
									blankedLetters.push(k - j);
									if (count['_'] < blankedLetters.size()) break;
								}
								else {
									flag = false;
									break;
								}
							}
							else count[ch]--;
							++needSize;
						}
					}
					if (count['_'] < blankedLetters.size()) flag = false;

					if (!flag || needSize == word.size() || !needSize) continue;
					if (j && matrix[i][j - 1] != ' ') continue;
					if (j + word.size() < 15 && matrix[i][j + word.size()] != ' ') continue;
					for (int k = j; k < j + word.size(); ++k) {
						if (i && matrix[i][k] == ' ' && matrix[i - 1][k] != ' ') flag = false;
						if (i + 1 < 15 && matrix[i][k] == ' ' && matrix[i + 1][k] != ' ') flag = false;
					}
					if (!flag) continue;

					int score = 0;
					bool isDoubleWord = false;
					bool isTripleWord = false;
					for (int k = j; k < j + word.size(); ++k) {
						int c = cost[word[k - j]];
						int col = getMultiplicator(i, k);
						if (!blankedLetters.empty() && k - j == blankedLetters.front()) {
							c = cost['_'];
							blankedLetters.pop();
						}
						score += c;
						if (matrix[i][k] != ' ') continue;
						if (col == 2) score += c;
						if (col == 3) score += 2 * c;
						if (col == 22) isDoubleWord = true;
						if (col == 33) isTripleWord = true;
					}
					if (isDoubleWord) score *= 2;
					if (isTripleWord) score *= 3;

					Word noun(word, i, j, true, score, wordInd);
					words.emplace_back(noun);

					++cnt;
				}
			}
			// try to put word vertically
			for (int j = 0; j < 15; ++j) {
				for (int i = 0; i < 15 - word.size() + 1; ++i) {
					bool flag = true; int needSize = 0;
					vector<int> count(256); queue<int> blankedLetters;
					for (char ch : letters) count[ch]++;
					for (int k = i; k < i + word.size(); ++k) {
						if (matrix[k][j] != ' ') {
							if (matrix[k][j] != word[k - i]) {
								flag = false;
								break;
							}
						}
						else {
							char ch = word[k - i];
							if (count[ch] <= 0) {
								if (count['_']) {
									blankedLetters.push(k - i);
									if (count['_'] < blankedLetters.size()) break;
								}
								else {
									flag = false;
									break;
								}
							}
							else count[ch]--;
							needSize++;
						}
					}
					if (count['_'] < blankedLetters.size()) flag = false;

					if (!flag || needSize == word.size() || !needSize) continue;
					if (i && matrix[i - 1][j] != ' ') continue;
					if (i + word.size() < 15 && 
						matrix[i + word.size()][j] != ' ') continue;
					for (int k = i; k < i + word.size(); ++k) {
						if (j && matrix[k][j] == ' ' && matrix[k][j - 1] != ' ') {
							flag = false;
							break;
						}
						if (j + 1 < 15 && matrix[k][j] == ' ' && matrix[k][j + 1] != ' ') {
							flag = false;
							break;
						}
					}
					if (!flag) continue;

					int score = 0;
					bool isDoubleWord = false;
					bool isTripleWord = false;
					for (int k = i; k < i + word.size(); ++k) {
						int c = cost[word[k - i]];
						int col = getMultiplicator(k, j);
						if (!blankedLetters.empty() && k - i == blankedLetters.front()) {
							c = cost['_'];
							blankedLetters.pop();
						}
						score += c;
						if (matrix[k][j] != ' ') continue;
						if (col == 2) score += c;
						if (col == 3) score += 2 * c;
						if (col == 22) isDoubleWord = true;
						if (col == 33) isTripleWord = true;
					}
					if (isDoubleWord) score *= 2;
					if (isTripleWord) score *= 3;

					Word noun(word, i, j, false, score, wordInd);
					words.emplace_back(noun);

					++cnt;
				}
			}
		}
		cout << "words size : " << words.size() << endl;
		// sort words by their costs
		sort(words.begin(), words.end(), [](const Word& a,
			const Word& b) {
				if (a.score == b.score) return a.word < b.word;
				return a.score > b.score;
			}
		);
		for (int i = 0; i < min(cnt, wordsInSolution); ++i) {
			Word noun = words[i];
			
			f << noun.word << '\n';
			f << noun.i << '\n';
			f << noun.j << '\n';
			f << noun.score << '\n';
			f << (noun.h ? 'h' : 'v') << '\n';
			f << noun.wordInd << '\n';
		}
		f.close();
		cout << "done" << endl;
		return cnt;
	}
}

// Copyright 2023 <Gustavo Beretta Gonçalves>

#ifndef STRUCTURES_ARRAY_LIST_H
#define STRUCTURES_ARRAY_LIST_H

#include <cstdint>
#include <cstddef>


namespace structures {

template<typename T>
class ArrayList {
 public:
    ArrayList();
    explicit ArrayList(std::size_t max_size);
    ~ArrayList();

    void clear();
    void push_back(const T& data);
    void push_front(const T& data);
    void insert(const T& data, std::size_t index);
    void insert_sorted(const T& data);
    T pop(std::size_t index);
    T pop_back();
    T pop_front();
    void remove(const T& data);
    bool full() const;
    bool empty() const;
    bool contains(const T& data) const;
    std::size_t find(const T& data) const;
    std::size_t size() const;
    std::size_t max_size() const;
    T& at(std::size_t index);
    T& operator[](std::size_t index);
    const T& at(std::size_t index) const;
    const T& operator[](std::size_t index) const;
    // descricao do 'operator []' na FAQ da disciplina

 private:
    T* contents;
    std::size_t size_;
    std::size_t max_size_;
    static const auto DEFAULT_MAX = 10u;
};

template<typename T>
ArrayList<T>::ArrayList() {
    size_ = 0;
    max_size_ = DEFAULT_MAX;
    contents = new T[max_size_];
}

template<typename T>
ArrayList<T>::ArrayList(std::size_t max_size) {
    size_ = 0;
    max_size_ = max_size;
    contents = new T[max_size_];
}

template<typename T>
ArrayList<T>::~ArrayList() {
    delete[] contents;
}

template<typename T>
void ArrayList<T>::clear() {
    size_ = 0;
}

template<typename T>
void ArrayList<T>::push_back(const T& data) {
    insert(data, size_);
}

template<typename T>
void ArrayList<T>::push_front(const T& data) {
    insert(data, 0);
}

template<typename T>
void ArrayList<T>::insert(const T& data, std::size_t index) {
    if (full()) {
        throw std::out_of_range("Lista cheia");
    }

    if (index > size_) {
        throw std::out_of_range("Índice inválido");
    }

    for (auto i = size_; i > index; --i) {
        contents[i] = contents[i - 1];
    }

    contents[index] = data;
    ++size_;
}

template<typename T>
void ArrayList<T>::insert_sorted(const T& data) {
    auto i = 0u;
    while (i < size_ && data > contents[i]) {
        ++i;
    }
    insert(data, i);
}

template<typename T>
T ArrayList<T>::pop(std::size_t index) {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    if (index >= size_) {
        throw std::out_of_range("Índice inválido");
    }

    auto data = contents[index];
    for (auto i = index; i < size_ - 1; ++i) {
        contents[i] = contents[i + 1];
    }
    --size_;
    return data;
}

template<typename T>
T ArrayList<T>::pop_back() {
    return pop(size_ - 1);
}

template<typename T>
T ArrayList<T>::pop_front() {
    return pop(0);
}

template<typename T>
void ArrayList<T>::remove(const T& data) {
    auto index = find(data);
    if (index != size_) {
        pop(index);
}
}

template<typename T>
bool ArrayList<T>::full() const {
        return size_ == max_size_;
}

template<typename T>
bool ArrayList<T>::empty() const {
    return size_ == 0;
}

template<typename T>
bool ArrayList<T>::contains(const T& data) const {
    return find(data) != size_;
}

template<typename T>
std::size_t ArrayList<T>::find(const T& data) const {
    for (auto i = 0u; i < size_; ++i) {
        if (data == contents[i]) {
            return i;
        }
    }
    return size_;
}

template<typename T>
std::size_t ArrayList<T>::size() const {
    return size_;
}

template<typename T>
std::size_t ArrayList<T>::max_size() const {
    return max_size_;
}

template<typename T>
T& ArrayList<T>::at(std::size_t index) {
    if (index >= size_) {
        throw std::out_of_range("Índice inválido");
    }
    return contents[index];
}

template<typename T>
T& ArrayList<T>::operator[](std::size_t index) {
    return at(index);
}

template<typename T>
const T& ArrayList<T>::at(std::size_t index) const {
    if (index >= size_) {
        throw std::out_of_range("Índice inválido");
    }
    return contents[index];
}

template<typename T>
const T& ArrayList<T>::operator[](std::size_t index) const {
    return at(index);
}

}  // namespace structures

#endif

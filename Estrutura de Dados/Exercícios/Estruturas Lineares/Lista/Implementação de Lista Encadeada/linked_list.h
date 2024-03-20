//! Copyright 2023 <Gustavo Beretta Gonçalves>

#ifndef STRUCTURES_LINKED_LIST_H
#define STRUCTURES_LINKED_LIST_H

#include <cstdint>
#include <cstddef>


namespace structures {

//! ...
template<typename T>
class LinkedList {
 public:
    //! ...
    LinkedList();  // construtor padrão
    //! ...
    ~LinkedList();  // destrutor
    //! ...
    void clear();  // limpar lista
    //! ...
    void push_back(const T& data);  // inserir no fim
    //! ...
    void push_front(const T& data);  // inserir no início
    //! ...
    void insert(const T& data, std::size_t index);  // inserir na posição
    //! ...
    void insert_sorted(const T& data);  // inserir em ordem
    //! ...
    T& at(std::size_t index);  // acessar um elemento na posição index
    //! ...
    T pop(std::size_t index);  // retirar da posição
    //! ...
    T pop_back();  // retirar do fim
    //! ...
    T pop_front();  // retirar do início
    //! ...
    void remove(const T& data);  // remover específico
    //! ...
    bool empty() const;  // lista vazia
    //! ...
    bool contains(const T& data) const;  // contém
    //! ...
    std::size_t find(const T& data) const;  // posição do dado
    //! ...
    std::size_t size() const;  // tamanho da lista

 private:
    class Node {  // Elemento
     public:
        explicit Node(const T& data):
            data_{data}
        {}

        Node(const T& data, Node* next):
            data_{data},
            next_{next}
        {}

        T& data() {  // getter: dado
            return data_;
        }

        const T& data() const {  // getter const: dado
            return data_;
        }

        Node* next() {  // getter: próximo
            return next_;
        }

        const Node* next() const {  // getter const: próximo
            return next_;
        }

        void next(Node* node) {  // setter: próximo
            next_ = node;
        }

     private:
        T data_;
        Node* next_{nullptr};
    };

    Node* end() {  // último nodo da lista
        auto it = head;
        for (auto i = 1u; i < size(); ++i) {
            it = it->next();
        }
        return it;
    }

    Node* head{nullptr};
    std::size_t size_{0u};
};

}  // namespace structures

template<typename T>
structures::LinkedList<T>::LinkedList() {
    head = nullptr;
    size_ = 0;
}
//! ...
template<typename T>
structures::LinkedList<T>::~LinkedList() {
    clear();
}
template<typename T>
void structures::LinkedList<T>::clear() {
    Node* next;
    Node* current = head;
    for (std::size_t i = 0; i < size_; i++) {
        next = current->next();
        delete current;
        current = next;
    }
    size_ = 0;
}
template<typename T>
void structures::LinkedList<T>::push_back(const T& data) {
    Node *n = new Node(data, nullptr);
    if (size_ == 0) {
        head = n;
        ++size_;
        return;
    }
    Node *end = head;
    for (std::size_t i = 1; i < size_; i++) {
        end = end->next();
    }
    end->next(n);
    ++size_;
}
template<typename T>
void structures::LinkedList<T>::push_front(const T& data) {
    Node *previous_head = head;
    head = new Node(data, previous_head);
    ++size_;
}
template<typename T>
void structures::LinkedList<T>::insert(const T& data, std::size_t index) {
    if (index >= size_ || index < 0) throw std::out_of_range("index fora do range");
    Node *insert = new Node(data, nullptr);
    if (!index) {
        head = insert;
        ++size_;
        return;
    }
    Node *previous = nullptr;
    Node *current = head;
    for (std::size_t i = 0; i < index; i++) {
        previous = current;
        current = current->next();
    }
    previous->next(insert);
    insert->next(current);
    ++size_;
}
template<typename T>
void structures::LinkedList<T>::insert_sorted(const T& data) {
    Node *insert = new Node(data, head);
    if (!size_ || head->data() > data) {
        head = insert;
        ++size_;
        return;
    }
    Node *previous = nullptr;
    Node *current = head;
    for (std::size_t i = 0; i < size_; i++) {
        if (current->data() > data) {
            break;
        }
        previous = current;
        current = current->next();
    }
    previous->next(insert);
    insert->next(current);
    ++size_;
}
template<typename T>
T& structures::LinkedList<T>::at(std::size_t index) {
    if (index >= size_ || index < 0) throw std::out_of_range("index fora do range");
    Node *n = head;
    for (std::size_t i = 0; i < index; i++) {
        n = n->next();
    }
    return n->data();
}
template<typename T>
T structures::LinkedList<T>::pop(std::size_t index) {
    if (empty()) throw std::out_of_range("lista vazia");
    if (index >= size_ || index < 0) throw std::out_of_range("index fora do range");
    if (index == 0) {
        Node *previous_head = head;
        head = previous_head->next();
        --size_;
        return previous_head->data();
    }
    Node *previous = nullptr;
    Node *current = head;
    for (std::size_t i = 0; i < index; i++) {
        previous = current;
        current = current->next();
    }
    previous->next(current->next());
    --size_;
    return current->data();
}
template<typename T>
T structures::LinkedList<T>::pop_back() {
    return pop(size_ - 1);
}
template<typename T>
T structures::LinkedList<T>::pop_front() {
    return pop(0);
}
template<typename T>
void structures::LinkedList<T>::remove(const T& data) {
    Node *n = head;
    for (std::size_t i = 0; i < size_; i++) {
        if (n->data() == data) {
            pop(i);
            return;
        }
        n = n->next();
    }
}
template<typename T>
bool structures::LinkedList<T>::empty() const {
    return (size_ == 0);
}
template<typename T>
bool structures::LinkedList<T>::contains(const T& data) const {
    Node *n = head;
    for (std::size_t i = 0; i < size_; i++) {
        if (n->data() == data) {
            return true;
        }
        n = n->next();
    }
    return false;
}
template<typename T>
std::size_t structures::LinkedList<T>::find(const T& data) const {
    Node *n = head;
    for (std::size_t i = 0; i < size_; i++) {
        if (n->data() == data) {
            return i;
        }
        n = n->next();
    }
    return size_;
}
template<typename T>
std::size_t structures::LinkedList<T>::size() const {
    return size_;
}

#endif

// Copyright 2023 <Gustavo Beretta Gonçalves>

#include <cstddef>

namespace structures {

template<typename T>
class DoublyCircularList {
 public:
    DoublyCircularList();
    ~DoublyCircularList();

    void clear();

    void push_back(const T& data);  // insere no fim
    void push_front(const T& data);  // insere no início
    void insert(const T& data, std::size_t index);  // insere na posição
    void insert_sorted(const T& data);  // insere em ordem

    T pop(std::size_t index);  // retira da posição
    T pop_back();  // retira do fim
    T pop_front();  // retira do início
    void remove(const T& data);  // retira específico

    bool empty() const;  // lista vazia
    bool contains(const T& data) const;  // contém

    T& at(std::size_t index);  // acesso a um elemento (checando limites)
    const T& at(std::size_t index) const;  // getter constante a um elemento

    std::size_t find(const T& data) const;  // posição de um dado
    std::size_t size() const;  // tamanho

 private:
    class Node {
     public:
        explicit Node(const T& data);
        Node(const T& data, Node* next);
        Node(const T& data, Node* prev, Node* next);

        T& data();
        const T& data() const;

        Node* prev();
        const Node* prev() const;

        void prev(Node* node);

        Node* next();
        const Node* next() const;

        void next(Node* node);

     private:
        T data_;
        Node* prev_;
        Node* next_;
    };

    Node* head;
    std::size_t size_;
};

template<typename T>
structures::DoublyCircularList<T>::DoublyCircularList() {
    head = nullptr;
    size_ = 0;
}

template<typename T>
structures::DoublyCircularList<T>::~DoublyCircularList() {
    clear();
}

template<typename T>
void structures::DoublyCircularList<T>::clear() {
    while (!empty()) {
        pop_front();
    }
}

template<typename T>
void structures::DoublyCircularList<T>::push_back(const T& data) {
    Node* novo = new Node(data);
    if (empty()) {
        head = novo;
        head -> next(novo);
        head -> prev(novo);
    } else {
        Node* ultimo = head -> prev();
        novo -> prev(ultimo);
        novo -> next(head);
        ultimo -> next(novo);
        head -> prev(novo);
    }
    size_++;
}

template<typename T>
void structures::DoublyCircularList<T>::push_front(const T& data) {
    Node* novo = new Node(data);
    if (empty()) {
        head = novo;
        head -> next(novo);
        head -> prev(novo);
    } else {
        Node* ultimo = head->prev();
        novo -> prev(ultimo);
        novo -> next(head);
        ultimo -> next(novo);
        head -> prev(novo);
        head = novo;
    }
    size_++;
}

template<typename T>
void structures::DoublyCircularList<T>::insert(const T& data,
                                                    std::size_t index) {
    if (index > size_) {
        throw std::out_of_range("Index fora do range");
    }

    if (index == 0) {
        push_front(data);
    } else if (index == size_) {
        push_back(data);
    } else {
        Node* novo = new Node(data);
        Node* atual = head;
        for (std::size_t i = 0; i < index - 1; i++) {
            atual = atual -> next();
        }
        novo -> prev(atual);
        novo -> next(atual -> next());
        atual -> next()->prev(novo);
        atual -> next(novo);
        size_++;
    }
}

template<typename T>
void structures::DoublyCircularList<T>::insert_sorted(const T& data) {
    Node* novo = new Node(data);
    if (empty()) {
        head = novo;
        head -> next(novo);
        head -> prev(novo);
    } else {
        Node* atual = head;
        while (atual -> next() != head && data > atual -> next() -> data()) {
            atual = atual->next();
        }
        if (data > atual -> data()) {
            novo -> next(atual -> next());
            novo -> prev(atual);
            atual -> next() -> prev(novo);
            atual -> next(novo);
        } else {
            novo -> next(atual);
            novo -> prev(atual -> prev());
            atual -> prev()->next(novo);
            atual -> prev(novo);
            if (atual == head) {
                head = novo;
            }
        }
    }
    size_++;
}



template<typename T>
T structures::DoublyCircularList<T>::pop(std::size_t index) {
    if (index >= size_) {
        throw std::out_of_range("Index fora do range");
    }

    if (index == 0) {
        return pop_front();
    } else if (index == size_ - 1) {
        return pop_back();
    } else {
        Node* atual = head;
        for (std::size_t i = 0; i < index; i++) {
            atual = atual -> next();
        }
        T pop_data = atual -> data();
        atual -> prev() -> next(atual -> next());
        atual -> next()->prev(atual -> prev());
        delete atual;
        size_--;
        return pop_data;
    }
}

template<typename T>
T structures::DoublyCircularList<T>::pop_back() {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    if (size_ == 1) {
        T pop_data = head -> data();
        delete head;
        head = nullptr;
        size_ = 0;
        return pop_data;
    } else {
        Node* ultimo = head->prev();
        T pop_data = ultimo -> data();
        ultimo -> prev() -> next(head);
        head -> prev(ultimo -> prev());
        delete ultimo;
        size_--;
        return pop_data;
    }
}

template<typename T>
T structures::DoublyCircularList<T>::pop_front() {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    if (size_ == 1) {
        T pop_data = head->data();
        delete head;
        head = nullptr;
        size_ = 0;
        return pop_data;
    } else {
        Node* primeiro = head;
        T pop_data = primeiro->data();
        primeiro->next()->prev(head->prev());
        head->prev()->next(primeiro->next());
        head = primeiro->next();
        delete primeiro;
        size_--;
        return pop_data;
    }
}

template<typename T>
void structures::DoublyCircularList<T>::remove(const T& data) {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    Node* atual = head;
    while (atual -> next() != head) {
        if (atual -> data() == data) {
            atual -> prev() -> next(atual -> next());
            atual -> next()->prev(atual -> prev());
            if (atual == head) {
                head = atual -> next();
            }
            delete atual;
            size_--;
            return;
        }
        atual = atual -> next();
    }

    if (atual -> data() == data) {
        atual -> prev()->next(atual -> next());
        atual -> next()->prev(atual -> prev());
        if (atual == head) {
            head = nullptr;
        }
        delete atual;
        size_--;
    }
}

template<typename T>
bool structures::DoublyCircularList<T>::empty() const {
    return size_ == 0;
}

template<typename T>
bool structures::DoublyCircularList<T>::contains(const T& data) const {
    if (empty()) {
        return false;
    }

    Node* atual = head;
    while (atual -> next() != head) {
        if (atual -> data() == data) {
            return true;
        }
        atual = atual->next();
    }

    if (atual -> data() == data) {
        return true;
    }

    return false;
}

template<typename T>
T& structures::DoublyCircularList<T>::at(std::size_t index) {
    if (index >= size_) {
        throw std::out_of_range("Index fora do range");
    }

    Node* atual = head;
    for (std::size_t i = 0; i < index; i++) {
        atual = atual -> next();
    }
    return atual -> data();
}

template<typename T>
const T& structures::DoublyCircularList<T>::at(std::size_t index) const {
    if (index >= size_) {
        throw std::out_of_range("Index fora do range");
    }

    const Node* atual = head;
    for (std::size_t i = 0; i < index; i++) {
        atual = atual -> next();
    }
    return atual -> data();
}

template<typename T>
std::size_t structures::DoublyCircularList<T>::find(const T& data) const {
    if (empty()) {
        return size_;
    }

    Node* atual = head;
    std::size_t index = 0;
    while (atual -> next() != head) {
        if (atual -> data() == data) {
            return index;
        }
        atual = atual -> next();
        index++;
    }

    if (atual -> data() == data) {
        return index;
    }

    return size_;
}

template<typename T>
std::size_t structures::DoublyCircularList<T>::size() const {
    return size_;
}

template<typename T>
structures::DoublyCircularList<T>::Node::Node(const T& data)
    : data_(data), prev_(nullptr), next_(nullptr) {}

template<typename T>
structures::DoublyCircularList<T>::Node::Node(const T& data, Node* next)
    : data_(data), prev_(nullptr), next_(next) {}

template<typename T>
structures::DoublyCircularList<T>::Node::Node(const T& data,
                                            Node* prev, Node* next)
    : data_(data), prev_(prev), next_(next) {}

template<typename T>
T& structures::DoublyCircularList<T>::Node::data() {
    return data_;
}

template<typename T>
const T& structures::DoublyCircularList<T>::Node::data() const {
    return data_;
}

template<typename T>
typename structures::DoublyCircularList<T>::Node* DoublyCircularList<T>
                                                    ::Node::prev() {
    return prev_;
}

template<typename T>
const typename structures::DoublyCircularList<T>::Node* DoublyCircularList<T>
                                                    ::Node::prev() const {
    return prev_;
}

template<typename T>
void structures::DoublyCircularList<T>::Node::prev(Node* node) {
    prev_ = node;
}

template<typename T>
typename structures::DoublyCircularList<T>::Node* DoublyCircularList<T>
                                                    ::Node::next() {
    return next_;
}

template<typename T>
const typename structures::DoublyCircularList<T>::Node* DoublyCircularList<T>
                                                        ::Node::next() const {
    return next_;
}

template<typename T>
void structures::DoublyCircularList<T>::Node::next(Node* node) {
    next_ = node;
}
}  // namespace structures

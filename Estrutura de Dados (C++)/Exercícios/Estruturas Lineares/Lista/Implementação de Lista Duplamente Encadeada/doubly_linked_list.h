// Copyright 2023 <Gustavo Beretta Gonçalves>

namespace structures {

template<typename T>
class DoublyLinkedList {
 public:
    DoublyLinkedList();
    ~DoublyLinkedList();
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
    class Node {  // implementar cada um dos métodos de Node
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

    Node* head;  // primeiro da lista
    Node* tail;  // ultimo da lista
    std::size_t size_;
};


template<typename T>
structures::DoublyLinkedList<T>::DoublyLinkedList() {
    head = nullptr;
    tail = nullptr;
    size_ = 0;
}

template<typename T>
structures::DoublyLinkedList<T>::~DoublyLinkedList() {
    clear();
}

template<typename T>
void structures::DoublyLinkedList<T>::clear() {
    Node* atual = head;
    while (atual != nullptr) {
        Node* next = atual -> next();
        delete atual;
        atual = next;
    }
    head = nullptr;
    tail = nullptr;
    size_ = 0;
}

template<typename T>
void structures::DoublyLinkedList<T>::push_back(const T& data) {
    Node* new_node = new Node(data);
    if (empty()) {
        head = new_node;
        tail = new_node;
    } else {
        tail -> next(new_node);
        new_node -> prev(tail);
        tail = new_node;
    }
    size_++;
}

template<typename T>
void structures::DoublyLinkedList<T>::push_front(const T& data) {
    Node* new_node = new Node(data);
    if (empty()) {
        head = new_node;
        tail = new_node;
    } else {
        new_node -> next(head);
        head -> prev(new_node);
        head = new_node;
    }
    size_++;
}

template<typename T>
void structures::DoublyLinkedList<T>::insert(const T& data, std::size_t index) {
    if (index > size_) {
        throw std::out_of_range("Index fora do range");
    }

    if (index == 0) {
        push_front(data);
    } else if (index == size_) {
        push_back(data);
    } else {
        Node* new_node = new Node(data);
        Node* atual = head;
        for (std::size_t i = 0; i < index - 1; i++) {
            atual = atual -> next();
        }
        new_node -> prev(atual);
        new_node -> next(atual->next());
        atual -> next() -> prev(new_node);
        atual -> next(new_node);
        size_++;
    }
}

template<typename T>
void structures::DoublyLinkedList<T>::insert_sorted(const T& data) {
    Node* new_node = new Node(data);
    if (empty() || data <= head->data()) {
        push_front(data);
        delete new_node;
    } else if (data >= tail->data()) {
        push_back(data);
        delete new_node;
    } else {
        Node* atual = head;
        while (atual -> next() != nullptr && data > atual->next() ->
                                                                data()) {
            atual = atual -> next();
        }
        new_node->prev(atual);
        new_node->next(atual->next());
        atual->next()->prev(new_node);
        atual->next(new_node);
        size_++;
    }
}

template<typename T>
T structures::DoublyLinkedList<T>::pop(std::size_t index) {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }
    if (index >= size_) {
        throw std::out_of_range("Index fora do range");
    }

    T data;
    if (index == 0) {
        data = pop_front();
    } else if (index == size_ - 1) {
        data = pop_back();
    } else {
        Node* atual = head;
        for (std::size_t i = 0; i < index; i++) {
            atual = atual -> next();
        }
        Node* prev_node = atual -> prev();
        Node* next_node = atual -> next();
        data = atual -> data();
        prev_node -> next(next_node);
        next_node -> prev(prev_node);
        delete atual;
        size_--;
    }
    return data;
}

template<typename T>
T structures::DoublyLinkedList<T>::pop_back() {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    T data = tail -> data();
    if (size_ == 1) {
        delete tail;
        head = nullptr;
        tail = nullptr;
    } else {
        Node* prev_node = tail -> prev();
        prev_node -> next(nullptr);
        delete tail;
        tail = prev_node;
    }
    size_--;
    return data;
}

template<typename T>
T structures::DoublyLinkedList<T>::pop_front() {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    T data = head->data();
    if (size_ == 1) {
        delete head;
        head = nullptr;
        tail = nullptr;
    } else {
        Node* next_node = head -> next();
        next_node -> prev(nullptr);
        delete head;
        head = next_node;
    }
    size_--;
    return data;
}

template<typename T>
void structures::DoublyLinkedList<T>::remove(const T& data) {
    if (empty()) {
        throw std::out_of_range("Lista vazia");
    }

    Node* atual = head;
    while (atual != nullptr && atual -> data() != data) {
        atual = atual -> next();
    }

    if (atual == nullptr) {
        throw std::invalid_argument("Dado invalido");
    }

    Node* prev_node = atual -> prev();
    Node* next_node = atual -> next();

    if (prev_node != nullptr) {
        prev_node -> next(next_node);
    } else {
        head = next_node;
    }

    if (next_node != nullptr) {
        next_node -> prev(prev_node);
    } else {
        tail = prev_node;
    }

    delete atual;
    size_--;
}

template<typename T>
bool structures::DoublyLinkedList<T>::empty() const {
    return size_ == 0;
}

template<typename T>
bool structures::DoublyLinkedList<T>::contains(const T& data) const {
    Node* atual = head;
    while (atual != nullptr) {
        if (atual -> data() == data) {
            return true;
        }
        atual = atual -> next();
    }
    return false;
}

template<typename T>
T& structures::DoublyLinkedList<T>::at(std::size_t index) {
    if (index >= size_) {
        throw std::out_of_range("Index fora do range");
    }

    Node* atual = head;
    for (std::size_t i = 0; i < index; i++) {
        atual = atual->next();
    }
    return atual -> data();
}

template<typename T>
const T& structures::DoublyLinkedList<T>::at(std::size_t index) const {
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
std::size_t structures::DoublyLinkedList<T>::find(const T& data) const {
    Node* atual = head;
    std::size_t index = 0;
    while (atual != nullptr) {
        if (atual -> data() == data) {
            return index;
        }
        atual = atual -> next();
        index++;
    }
    return size_;
}

template<typename T>
std::size_t structures::DoublyLinkedList<T>::size() const {
    return size_;
}

template<typename T>
structures::DoublyLinkedList<T>::Node::Node(const T& data)
    : data_(data), prev_(nullptr), next_(nullptr) {}

template<typename T>
structures::DoublyLinkedList<T>::Node::Node(const T& data, Node* next)
    : data_(data), prev_(nullptr), next_(next) {}

template<typename T>
structures::DoublyLinkedList<T>::Node::Node(const T& data, Node* prev,
                                                                Node* next)
    : data_(data), prev_(prev), next_(next) {}

template<typename T>
T& structures::DoublyLinkedList<T>::Node::data() {
    return data_;
}

template<typename T>
const T& structures::DoublyLinkedList<T>::Node::data() const {
    return data_;
}

template<typename T>
typename structures::DoublyLinkedList<T>::Node* DoublyLinkedList<T>::
                                                            Node::prev() {
    return prev_;
}

template<typename T>
const typename structures::DoublyLinkedList<T>::Node* DoublyLinkedList<T>::
                                                        Node::prev() const {
    return prev_;
}

template<typename T>
void structures::DoublyLinkedList<T>::Node::prev(Node* node) {
    prev_ = node;
}

template<typename T>
typename structures::DoublyLinkedList<T>::Node* DoublyLinkedList<T>::
                                                            Node::next() {
    return next_;
}

template<typename T>
const typename structures::DoublyLinkedList<T>::Node* DoublyLinkedList<T>::
                                                    Node::next() const {
    return next_;
}

template<typename T>
void structures::DoublyLinkedList<T>::Node::next(Node* node) {
    next_ = node;
}
}  // namespace structures

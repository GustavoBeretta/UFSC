// Copyright 2023 <Gustavo Beretta Gonçalves>

#include "array_list.h"
#include <cstddef>

namespace structures {

template<typename T>
class BinaryTree {
public:
    BinaryTree();
    ~BinaryTree();

    void insert(const T& data);
    void remove(const T& data);
    bool contains(const T& data) const;
    bool empty() const;
    std::size_t size() const;
    ArrayList<T> pre_order() const;
    ArrayList<T> in_order() const;
    ArrayList<T> post_order() const;

private:
    struct Node {
        explicit Node(const T& data);
        T data;
        Node* left;
        Node* right;

        void insert(const T& data_);
        bool remove(const T& data_);
        bool contains(const T& data_) const;
        void pre_order(ArrayList<T>& v) const;
        void in_order(ArrayList<T>& v) const;
        void post_order(ArrayList<T>& v) const;
    };

    Node* root;
    std::size_t size_;
};

template<typename T>
BinaryTree<T>::BinaryTree() {
    root = nullptr;
    size_ = 0;
}

template<typename T>
BinaryTree<T>::~BinaryTree() {
    // TODO(user): Implementar a destruição da árvore.
}

template<typename T>
void structures::BinaryTree<T>::insert(const T& data) {
    if (empty()) {
        root = new Node(data);
    } else {
        root->insert(data);
    }
    size_++;
}

template<typename T>
void structures::BinaryTree<T>::remove(const T& data) {
    if (!empty()) {
        if (root->remove(data)) {
            size_--;
        }
    }
}

template<typename T>
bool structures::BinaryTree<T>::contains(const T& data) const {
    if (empty()) {
        return false;
    } else {
        return root->contains(data);
    }
}

template<typename T>
bool structures::BinaryTree<T>::empty() const {
    return size_ == 0;
}

template<typename T>
std::size_t structures::BinaryTree<T>::size() const {
    return size_;
}

template<typename T>
ArrayList<T> structures::BinaryTree<T>::pre_order() const {
    ArrayList<T> result;
    if (!empty()) {
        root->pre_order(result);
    }
    return result;
}

template<typename T>
ArrayList<T> structures::BinaryTree<T>::in_order() const {
    ArrayList<T> result;
    if (!empty()) {
        root->in_order(result);
    }
    return result;
}

template<typename T>
ArrayList<T> structures::BinaryTree<T>::post_order() const {
    ArrayList<T> result;
    if (!empty()) {
        root->post_order(result);
    }
    return result;
}

template<typename T>
structures::BinaryTree<T>::Node::Node(const T& data) {
    this->data = data;
    left = nullptr;
    right = nullptr;
}

template<typename T>
void structures::BinaryTree<T>::Node::insert(const T& data_) {
    if (data_ < data) {
        if (left == nullptr) {
            left = new Node(data_);
        } else {
            left->insert(data_);
        }
    } else {
        if (right == nullptr) {
            right = new Node(data_);
        } else {
            right->insert(data_);
        }
    }
}

template<typename T>
bool BinaryTree<T>::Node::remove(const T& data_) {
    if (data_ == data) {
        if (left != nullptr && right != nullptr) {
            Node* minimum = right;
            while (minimum->left != nullptr) {
                minimum = minimum->left;
            }
            data = minimum->data;
            return right->remove(data);
        } else {
            Node* old_node = this;
            if (left != nullptr) {
                *this = *left;
            } else if (right != nullptr) {
                *this = *right;
            } else {
                // Caso especial: remoção do nó raiz sem filhos
                return true;
            }
            delete old_node;
            return true;
        }
    } else if (data_ < data && left != nullptr) {
        if (left->remove(data_)) {
            left = nullptr;
        }
        return true;
    } else if (data_ > data && right != nullptr) {
        if (right->remove(data_)) {
            right = nullptr;
        }
        return true;
    }
    return false;
}

template<typename T>
bool structures::BinaryTree<T>::Node::contains(const T& data_) const {
    if (data_ == data) {
        return true;
    } else if (data_ < data && left != nullptr) {
        return left->contains(data_);
    } else if (data_ > data && right != nullptr) {
        return right->contains(data_);
    }
    return false;
}

template<typename T>
void structures::BinaryTree<T>::Node::pre_order(ArrayList<T>& v) const {
    v.push_back(data);
    if (left != nullptr) {
        left->pre_order(v);
    }
    if (right != nullptr) {
        right->pre_order(v);
    }
}

template<typename T>
void structures::BinaryTree<T>::Node::in_order(ArrayList<T>& v) const {
    if (left != nullptr) {
        left->in_order(v);
    }
    v.push_back(data);
    if (right != nullptr) {
        right->in_order(v);
    }
}

template<typename T>
void structures::BinaryTree<T>::Node::post_order(ArrayList<T>& v) const {
    if (left != nullptr) {
        left->post_order(v);
    }
    if (right != nullptr) {
        right->post_order(v);
    }
    v.push_back(data);
}

}  // namespace structures

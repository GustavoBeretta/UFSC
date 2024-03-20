// Copyright 2023 <Gustavo Beretta Gonçalves>

#ifndef STRUCTURES_AVL_TREE_H
#define STRUCTURES_AVL_TREE_H

#include <cstdint>  // std::size_t
#include <stdexcept>  // C++ Exceptions
#include <algorithm>
#include "array_list.h"

namespace structures {

template<typename T>
class AVLTree {
public:
    ~AVLTree();

    void insert(const T& data);

    void remove(const T& data);

    bool contains(const T& data) const;

    bool empty() const;

    std::size_t size() const;

    int height() const;

    ArrayList<T> pre_order() const;

    ArrayList<T> in_order() const;

    ArrayList<T> post_order() const;

private:
    struct Node {
        explicit Node(const T& data):
          data{data},
          height_{0},
          left{nullptr},
          right{nullptr}
        {}

        T data;
        int height_;
        Node* left;
        Node* right;

        ~Node() {
            delete left;
            delete right;
        }

        Node* insert(const T& data_) {
            if (data_ < data) {
                if (left == nullptr) {
                    left = new Node(data_);
                } else {
                    left = left->insert(data_);
                }
            } else {  // Caso data_ >= data
                if (right == nullptr) {
                    right = new Node(data_);
                } else {
                    right = right->insert(data_);
                }
            }
            updateHeight();
            return balance();
        }

        Node* remove(const T& data_) {
            if (data_ < data) {
                if (left != nullptr) {
                    left = left->remove(data_);
                }
            } else if (data_ > data) {
                if (right != nullptr) {
                    right = right->remove(data_);
                }
            } else {
                if (left == nullptr && right == nullptr) {  // Sem filhos
                    delete this;
                    return nullptr;
                } else if (right != nullptr) {  // Filho à direita
                    Node* temp = right;
                    delete this;
                    return temp;
                } else if (left != nullptr) {  // Filho à esquerda
                    Node* temp = left;
                    delete this;
                    return temp;
                } else {  // Dois filhos
                    Node* temp = right->minimum();
                    data = temp->data;
                    right = right->remove(data);
                }
            }
            updateHeight();
            return balance();
        }

		Node* minimum() {
			if (left == nullptr) {
				return this;
			} else {
				return left->minimum();
			}
		}

        bool contains(const T& data_) const {
			if (data_ == data) {
				return true;
			} else if (data_ < data) {
				if (left == nullptr) {
					return false;
				} else {
					return left->contains(data_);
				}
			} else {
				if (right == nullptr) {
					return false;
				} else {
					return right->contains(data_);
				}
			}
		}

        void updateHeight() {
			int left_height = left == nullptr ? -1 : left->height();
			int right_height = right == nullptr ? -1 : right->height();
			height_ = std::max(left_height, right_height) + 1;
		}

		Node* balance() {
            int balance_factor = (left ? left->height() : -1) -
                                 (right ? right->height() : -1);
            if (balance_factor > 1) {
                // Se o fator de balanceamento for maior que 1, a subárvore
                // esquerda é maior que a direita
                if (left && (left->left ? left->left->height() : -1) >=
                            (left->right ? left->right->height() : -1)) {
                    // Se a subárvore esquerda for mais alta que a da direita,
                    // é uma rotação simples
                    return simpleRight();
                } else {
                    // Se não, é uma rotação dupla
                    return doubleRight();
                }
            } else if (balance_factor < -1) {
                // Se o fator de balanceamento for menor que -1, a subárvore
                // direita é maior que a esquerda
                if (right && (right->right ? right->right->height() : -1) >=
                             (right->left ? right->left->height() : -1)) {
                    // Se a subárvore direita for mais alta que a da esquerda,
                    // é uma rotação simples
                    return simpleLeft();
                } else {
                    // Se não, é uma rotação dupla
                    return doubleLeft();
                }
            }
            return this;
        }

        Node* simpleLeft() {
			Node* pivot = right;
            right = pivot->left;
            pivot->left = this;
            updateHeight();
            pivot->updateHeight();
            return pivot;
		}

        Node* simpleRight() {
			Node* pivot = left;
			left = pivot->right;
			pivot->right = this;
			updateHeight();
			pivot->updateHeight();
			return pivot;
		}

        Node* doubleLeft() {
			right = right->simpleRight();
			return simpleLeft();
		}

        Node* doubleRight() {
			left = left->simpleLeft();
			return simpleRight();
		}

        void pre_order(ArrayList<T>& v) const {
            v.push_back(data);
            if (left != nullptr) {
                left->pre_order(v);
            }
            if (right != nullptr) {
                right->pre_order(v);
            }
        }

        void in_order(ArrayList<T>& v) const {
            if (left != nullptr) {
                left->in_order(v);
            }
            v.push_back(data);
            if (right != nullptr) {
                right->in_order(v);
            }
        }

        void post_order(ArrayList<T>& v) const {
            if (left != nullptr) {
                left->post_order(v);
            }
            if (right != nullptr) {
                right->post_order(v);
            }
            v.push_back(data);
        }

        int height() {
			return height_;
        }
    };

    Node* root;
    std::size_t size_;
};

};  // namespace structures
#endif

template<typename T>
structures::AVLTree<T>::~AVLTree() {
	delete root;
}

template<typename T>
void structures::AVLTree<T>::insert(const T& data) {
	if (empty()) {
		root = new Node(data);
	} else {
		root = root->insert(data);
	}
	size_++;
}

template<typename T>
void structures::AVLTree<T>::remove(const T& data) {
	if (empty()) {
		throw std::out_of_range("Empty tree");
	} else {
		size_--;
		root = root->remove(data);
	}
}

template<typename T>
bool structures::AVLTree<T>::contains(const T& data) const {
	if (empty()) {
		throw std::out_of_range("Empty tree");
	} else {
		return root->contains(data);
	}
	return false;
}

template<typename T>
bool structures::AVLTree<T>::empty() const {
	return size_ == 0;
}

template<typename T>
std::size_t structures::AVLTree<T>::size() const {
	return size_;
}

template<typename T>
int structures::AVLTree<T>::height() const {
	return root != nullptr ? root->height_ : -1;
}

template<typename T>
structures::ArrayList<T> structures::AVLTree<T>::pre_order() const {
	structures::ArrayList<T> v{};
	if (!empty()) {
		root->pre_order(v);
	}
	return v;
}

template<typename T>
structures::ArrayList<T> structures::AVLTree<T>::in_order() const {
	structures::ArrayList<T> v{};
	if (!empty()) {
		root->in_order(v);
	}
	return v;
}

template<typename T>
structures::ArrayList<T> structures::AVLTree<T>::post_order() const {
	structures::ArrayList<T> v{};
	if (!empty()) {
		root->post_order(v);
	}
	return v;
}

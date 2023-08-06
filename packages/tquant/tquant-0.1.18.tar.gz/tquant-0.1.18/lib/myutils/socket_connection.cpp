#include <iostream>
#include <algorithm>
#include <string>
#include <memory>
#include <thread>
#include <mutex>
#include <assert.h>
#include "myutils/socket_connection.h"
#include "myutils/socketutils.h"
#include "myutils/stringutils.h"
//#include "myutils/concurrentqueue.h"

using namespace myutils;

SocketConnection::SocketConnection()
{
}

SocketConnection::~SocketConnection()
{
    close();
}

bool SocketConnection::connect(const std::string& addr, Connection_Callback* callback)
{
    if (m_main_thread) return false;

    m_callback = callback;
    m_addr = make_shared<string>(addr);

    m_should_exit = false;
    m_main_thread = new thread(&SocketConnection::main_run, this);

    return true;
}

void SocketConnection::reconnect()
{
    return;

    if (m_main_thread) {
        m_should_exit = true;
        m_main_thread->join();
        m_main_thread = nullptr;
    }
    m_should_exit = false;
    m_main_thread = new thread(&SocketConnection::main_run, this);
}

void SocketConnection::close()
{
    if (m_main_thread) {
        m_should_exit = true;
        m_main_thread->join();
        m_main_thread = nullptr;
    }
}

void SocketConnection::send(const char* data, size_t size)
{
    unique_lock<mutex> lock(m_send_lock);

    if (m_socket == INVALID_SOCKET) return;;

//#ifdef _WIN32
#ifndef MSG_MORE
  #define MSG_MORE 0
#endif
    int32_t pkt_len = (int32_t)size;
    int r1 = ::send(m_socket, (const char*)&pkt_len, 4, MSG_MORE);
    int r2 = ::send(m_socket, data, pkt_len, 0);
    if (r1 != 4 || r2 != pkt_len){
        // FIXME:!
        perror("socket send error:");
    }
}

void SocketConnection::send(const std::string& data)
{
    send( data.c_str(), data.size());
}

bool SocketConnection::is_connected()
{
    return m_socket != INVALID_SOCKET;
}

void SocketConnection::main_run()
{
    auto idle_time = system_clock::now();
    while (!m_should_exit) {
        auto now = system_clock::now();
        if (now < idle_time || now - idle_time > seconds(1)) {
            idle_time = now;
            m_callback->on_idle();
        }

        if (m_socket == INVALID_SOCKET) {
            if (!do_connect()) {
                this_thread::sleep_for(milliseconds(100));
                continue;
            }
        }

        fd_set rset, wset;
        FD_ZERO(&rset);
        FD_ZERO(&wset);

        FD_SET(m_socket, &rset);
        SOCKET high_sock = m_socket;

        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 500 * 1000;
        int r = ::select((int)high_sock + 1, &rset, &wset, nullptr, &tv);
        //if (r == -1 || r == 0)
        if (m_should_exit) break;

        switch (r) {
            case 0:
                break;
            case -1:
                do_connect();
                break;
            default:
                if (r > 0 && FD_ISSET(m_socket, &rset))
                    do_recv();
                break;
        };
    }

    do_close("", false);
}

void SocketConnection::do_close(const char* reason, bool should_notify)
{
    std::cout<<"SockectConnection closed: " << reason << endl;

    if (m_socket != INVALID_SOCKET) {
        closesocket(m_socket);
        m_socket = INVALID_SOCKET;
        m_recv_size = 0;
        m_pkt_size = 0;

        if (should_notify)
            if (m_callback) m_callback->on_conn_status(false);
    }
}

void SocketConnection::do_recv()
{
    if (m_pkt_size == 0) {
        int32_t pkt_size;
        int r = recv(m_socket, (char*)&pkt_size, 4, 0);
        if (r == 4) {
            if (pkt_size < 0 || pkt_size > 100 * 1024 * 1024) {
                do_close("wrong pkt_size");
                return;
            }

            m_recv_size = 0;
            m_pkt_size = pkt_size;

            if (m_recv_buf.size() < (size_t)pkt_size) m_recv_buf.resize(pkt_size);
        }
        else if (is_EWOURLDBLOCK(r)) {
            return;
        }
        else {
            perror("recv error:");
            do_close("recv error");
            return;
        }
    }

    if (m_pkt_size) {
        int r = recv(m_socket, (char*)m_recv_buf.c_str() + m_recv_size, m_pkt_size - m_recv_size, 0);
        if (r > 0) {
            m_recv_size += r;
            if (m_recv_size == m_pkt_size) {
                this->m_callback->on_recv(m_recv_buf.c_str(), m_pkt_size);
                m_recv_size = 0;
                m_pkt_size = 0;
            }
        }
        else if (is_EWOURLDBLOCK(r)) {
            //return;
        }
        else {
            do_close("recv error");
        }
    }
}

bool SocketConnection::do_connect() 
{
    auto addr = m_addr;
    if (!addr) return false;

    m_pkt_size = 0;
    m_recv_size = 0;
    vector<string> ss;
    split(addr->c_str() + 6, ":", &ss);
    if (ss.size() != 2) return false;

    string ip = ss[0];
    int port = atoi(ss[1].c_str());

    SOCKET sock = myutils::connect_socket(ip.c_str(), port);
    if (sock == INVALID_SOCKET) return false;

    if (!myutils::check_connect(sock, 2)) {
        closesocket(sock);
        return false;
    }

    myutils::set_socket_nonblock(sock, true);

    int recv_buf_size = 1*1024*1024;
    int send_buf_size = 1*1024*1024;
    setsockopt(sock, SOL_SOCKET, SO_RCVBUF, (const char*)&recv_buf_size, sizeof(int));
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, (const char*)&send_buf_size, sizeof(int));

    m_socket = sock;
    if (m_callback)
        m_callback->on_conn_status(true);

//    {
//        unique_lock<mutex> lock(m_send_lock);
//        if (m_send_list.size() > 0 && m_send_list.front()->send_len) {
//            m_send_list.pop_front();
//            m_send_count--;
//        }
//    }
    return true;
}

//void SocketConnection::close()
//{
//    m_should_exit = true;
//
//    if (m_main_thread) {
//        char buf[1] = { 'D' };
//        ::send(m_cmd_client, buf, 1, 0);
//
//        if (m_main_thread->joinable())
//            m_main_thread->join();
//        delete m_main_thread;
//
//        m_main_thread = nullptr;
//    }
//
//    if (m_socket != INVALID_SOCKET) {
//        closesocket(m_socket);
//        m_socket = INVALID_SOCKET;
//    }
//}

//void SocketConnection::send(const char* data, size_t size)
//{
//    int32_t len = (int32_t)size;
//
//    auto pkt = make_shared<SendPkt>(4 + size);
//    char* p = (char*)pkt->buf.c_str();
//    ::memcpy(p, (const char*)&len, 4);
//    ::memcpy(p + 4, data, size);
//
//    {
//        unique_lock<mutex> lock(m_send_lock);
//        m_send_list.push_back(pkt);
//        m_send_count++;
//
//        char buf[1] = { 'S' };
//        ::send(m_cmd_client, buf, 1, 0);
//    }
//}
//
//void SocketConnection::do_send()
//{
//    if (!m_send_count) return;
//
//    shared_ptr<SendPkt> pkt;
//    {
//        unique_lock<mutex> lock(m_send_lock);
//        if (m_send_list.size() != 0)
//            pkt = m_send_list.front();
//    }
//    if (!pkt) return;
//
//    size_t left_len = pkt->buf.size() - pkt->send_len;
//    int r = ::send(m_socket, (char*)pkt->buf.c_str() + pkt->send_len, (int)left_len, 0);
//    if (r > 0) {
//        pkt->send_len += r;
//        if (pkt->send_len == pkt->buf.size()) {
//            unique_lock<mutex> lock(m_send_lock);
//            m_send_list.pop_front();
//            m_send_count--;
//        }
//    }
//    else if (is_EWOURLDBLOCK(r)) {
//        return;
//    }
//    else {
//        this->do_close("send error");
//    }
//}
//
//void SocketConnection::send(const string& data)
//{
//    send(data.c_str(), data.size());
//}


// Generated by gencpp from file dh_hand_driver/hand_state.msg
// DO NOT EDIT!


#ifndef DH_HAND_DRIVER_MESSAGE_HAND_STATE_H
#define DH_HAND_DRIVER_MESSAGE_HAND_STATE_H

#include <ros/service_traits.h>


#include <dh_hand_driver/hand_stateRequest.h>
#include <dh_hand_driver/hand_stateResponse.h>


namespace dh_hand_driver
{

struct hand_state
{

typedef hand_stateRequest Request;
typedef hand_stateResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct hand_state
} // namespace dh_hand_driver


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::dh_hand_driver::hand_state > {
  static const char* value()
  {
    return "1c500bfaa3cbade723148f8b1db86f48";
  }

  static const char* value(const ::dh_hand_driver::hand_state&) { return value(); }
};

template<>
struct DataType< ::dh_hand_driver::hand_state > {
  static const char* value()
  {
    return "dh_hand_driver/hand_state";
  }

  static const char* value(const ::dh_hand_driver::hand_state&) { return value(); }
};


// service_traits::MD5Sum< ::dh_hand_driver::hand_stateRequest> should match
// service_traits::MD5Sum< ::dh_hand_driver::hand_state >
template<>
struct MD5Sum< ::dh_hand_driver::hand_stateRequest>
{
  static const char* value()
  {
    return MD5Sum< ::dh_hand_driver::hand_state >::value();
  }
  static const char* value(const ::dh_hand_driver::hand_stateRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::dh_hand_driver::hand_stateRequest> should match
// service_traits::DataType< ::dh_hand_driver::hand_state >
template<>
struct DataType< ::dh_hand_driver::hand_stateRequest>
{
  static const char* value()
  {
    return DataType< ::dh_hand_driver::hand_state >::value();
  }
  static const char* value(const ::dh_hand_driver::hand_stateRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::dh_hand_driver::hand_stateResponse> should match
// service_traits::MD5Sum< ::dh_hand_driver::hand_state >
template<>
struct MD5Sum< ::dh_hand_driver::hand_stateResponse>
{
  static const char* value()
  {
    return MD5Sum< ::dh_hand_driver::hand_state >::value();
  }
  static const char* value(const ::dh_hand_driver::hand_stateResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::dh_hand_driver::hand_stateResponse> should match
// service_traits::DataType< ::dh_hand_driver::hand_state >
template<>
struct DataType< ::dh_hand_driver::hand_stateResponse>
{
  static const char* value()
  {
    return DataType< ::dh_hand_driver::hand_state >::value();
  }
  static const char* value(const ::dh_hand_driver::hand_stateResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // DH_HAND_DRIVER_MESSAGE_HAND_STATE_H

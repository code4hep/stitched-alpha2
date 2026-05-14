#include "FWCore/Concurrency/interface/WaitingThreadPool.h"

#include <cassert>
#include <string_view>

#include <pthread.h>

namespace {
  // pthread_setname_np() string length is limited to 16 characters,
  // including the null termination.
  constexpr auto poolName = "edm async pool";
  static_assert(std::string_view(poolName).size() < 16);
}

namespace edm::impl {
  WaitingThread::WaitingThread() {
    thread_ = std::thread(&WaitingThread::threadLoop, this);
  }

  WaitingThread::~WaitingThread() noexcept {
    // When we are shutting down, we don't care about any possible
    // system errors anymore
    CMS_SA_ALLOW try {
      stopThread();
      thread_.join();
    } catch (...) {
    }
  }

  void WaitingThread::threadLoop() noexcept {
    // Name this thread.  The two platforms have different signatures:
    //   Linux:  pthread_setname_np(pthread_t, const char*)  -- can name any thread
    //   macOS:  pthread_setname_np(const char*)             -- can only name calling thread
    // We therefore set the name here, inside the thread, which works on both.
#ifdef __APPLE__
    [[maybe_unused]] int err = pthread_setname_np(poolName);
#else
    [[maybe_unused]] int err = pthread_setname_np(pthread_self(), poolName);
#endif
    // The only documented error is ERANGE (name too long), guarded by the
    // static_assert above.  Assert anyway to catch any future surprises.
    assert(err == 0);

    std::unique_lock lk(mutex_);

    while (true) {
      cond_.wait(lk, [this]() { return static_cast<bool>(func_) or stopThread_; });
      if (stopThread_) {
        // There should be no way to stop the thread when it as the
        // func_ assigned, but let's make sure
        assert(not thisPtr_);
        break;
      }
      func_();
      // Must return this WaitingThread to the ReusableObjectHolder in
      // the WaitingThreadPool before resettting func_ (that holds the
      // WaitingTaskWithArenaHolder, that enables the progress in the
      // TBB thread pool) in order to meet the requirement of
      // ReusableObjectHolder destructor that there are no outstanding
      // objects.
      thisPtr_.reset();
      decltype(func_)().swap(func_);
    }
  }
}  // namespace edm::impl

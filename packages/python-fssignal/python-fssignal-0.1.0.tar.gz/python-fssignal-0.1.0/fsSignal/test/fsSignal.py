# Builtin modules
import os, unittest, signal as _signal
from threading import Lock, RLock, Timer, Thread
from time import monotonic, sleep
from typing import List
# Third party modules
# Local modules
from .. import Signal, KillSignal, T_Signal, SoftSignal, HardSignal
# Program
class SignalTest(unittest.TestCase):
	rootSignal:Signal
	@classmethod
	def setUpClass(self) -> None:
		self.rootSignal = Signal()
		return None
	def tearDown(self) -> None:
		self.rootSignal.reset()
		return None
	def killmeTimer(self) -> None:
		def suicide() -> None:
			os.kill(os.getpid(), _signal.SIGINT)
			return None
		Timer(1, suicide).start()
		return None
	def test_sleep(self) -> None:
		t = monotonic()
		self.rootSignal.sleep(2)
		self.assertGreater(monotonic()-t, 2.0)
		return None
	def test_sleepRaise(self) -> None:
		self.killmeTimer()
		with self.assertRaises(KillSignal):
			self.rootSignal.getSoftSignal().sleep(4, raiseOnKill=True)
		return None
	def test_iter(self) -> None:
		s = list(range(5))
		d:List[int] = []
		signal = self.rootSignal.getSoftSignal()
		self.killmeTimer()
		with self.assertRaises(KillSignal):
			for i in s:
				signal.sleep(0.5, raiseOnKill=True)
				d.append(i)
		return None
	def test_hardkill(self) -> None:
		self.killmeTimer()
		sleep(0.1)
		self.killmeTimer()
		sleep(0.1)
		self.killmeTimer()
		sleep(0.1)
		self.rootSignal.forceCounter = 3
		with self.assertRaises(KillSignal):
			self.rootSignal.sleep(10, raiseOnKill=True)
		self.rootSignal.forceCounter = 10
		return None
	def test_check(self) -> None:
		signal = self.rootSignal.getSoftSignal()
		signal.check()
		self.assertEqual(signal.get(), False)
		self.killmeTimer()
		signal.sleep(5, raiseOnKill=False)
		with self.assertRaises(KillSignal):
			signal.check()
		self.assertEqual(signal.get(), True)
	def test_lock(self) -> None:
		signal = self.rootSignal.getSoftSignal()
		locker = signal.warpLock(Lock())
		self.assertFalse(locker.owned())
		self.assertFalse(locker.locked())
		#
		self.assertTrue(locker.acquire())
		self.assertTrue(locker.owned())
		self.assertTrue(locker.locked())
		self.assertFalse(locker.acquire(timeout=0.1))
		#
		self.killmeTimer()
		with self.assertRaises(KillSignal):
			locker.acquire()
		locker.release()
		with self.assertRaises(RuntimeError):
			locker.release()
		return None
	def test_lockWith(self) -> None:
		signal = self.rootSignal.getSoftSignal()
		locker = signal.warpLock(Lock())
		with locker:
			self.assertFalse(locker.acquire(timeout=0.1))
			self.killmeTimer()
			with self.assertRaises(KillSignal):
				locker.acquire()
		return None
	def test_rlock(self) -> None:
		def AcquireAndSleep() -> None:
			with locker:
				sleep(5)
		signal = self.rootSignal.getSoftSignal()
		locker = signal.warpLock(RLock())
		self.assertFalse(locker.owned())
		self.assertFalse(locker.locked())
		#
		self.assertTrue(locker.acquire())
		self.assertTrue(locker.owned())
		self.assertTrue(locker.locked())
		self.assertTrue(locker.acquire(timeout=0.1))
		locker.release()
		locker.release()
		#
		self.assertFalse(locker.owned())
		self.assertFalse(locker.locked())
		thr = Thread(target=AcquireAndSleep, daemon=True)
		thr.start()
		signal.sleep(1)
		self.assertFalse(locker.owned())
		self.assertTrue(locker.locked())
		#
		self.killmeTimer()
		with self.assertRaises(KillSignal):
			locker.acquire()
		thr.join()
		with self.assertRaises(RuntimeError):
			locker.release()
		return None
	def test_rlockStress(self) -> None:
		signal = self.rootSignal.getSoftSignal()
		locker = signal.warpLock(RLock())
		for i in range(100):
			self.assertTrue(locker.acquire())
			self.assertTrue(locker.owned())
			self.assertTrue(locker.locked())
			locker.release()
	def test_types(self) -> None:
		signal:T_Signal
		signal = SoftSignal()
		signal = HardSignal()
		signal = self.rootSignal.getSoftSignal()
		signal = self.rootSignal.getHardSignal()
		signal = self.rootSignal
		signal

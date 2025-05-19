# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        next_head = self.removeNodes(head.next)

        if head.val < next_head.val:
            return next_head
        else:
            head.next = next_head
            return head
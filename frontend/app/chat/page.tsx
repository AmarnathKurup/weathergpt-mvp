import LocationSearchBar from "@/components/LocationSearchBar";
import ChatWindow from "@/components/ChatWindow";

export default function ChatPage() {
  return (
    <div className="flex flex-col gap-6">
      <LocationSearchBar />
      <ChatWindow />
    </div>
  );
}

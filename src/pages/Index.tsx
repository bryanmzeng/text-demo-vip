import { useState } from 'react';
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/components/ui/use-toast";
import { db, TextEntry } from '../db/database';
import { useLiveQuery } from 'dexie-react-hooks';
import { Trash2 } from 'lucide-react';

const Index = () => {
  const [newText, setNewText] = useState('');
  const { toast } = useToast();
  
  // Live query all entries, sorted by timestamp
  const entries = useLiveQuery(
    () => db.textEntries.orderBy('timestamp').reverse().toArray(),
    []
  );

  const handleSubmit = async () => {
    if (!newText.trim()) {
      toast({
        title: "Error",
        description: "Please enter some text",
        variant: "destructive",
      });
      return;
    }

    try {
      await db.textEntries.add({
        content: newText,
        timestamp: new Date(),
      });
      
      setNewText('');
      toast({
        title: "Success",
        description: "Text entry saved successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save text entry",
        variant: "destructive",
      });
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await db.textEntries.delete(id);
      toast({
        title: "Success",
        description: "Entry deleted successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete entry",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen p-4 max-w-2xl mx-auto space-y-6">
      <div className="space-y-4">
        <h1 className="text-2xl font-bold">Text Entry Demo</h1>
        
        <div className="space-y-2">
          <Textarea
            value={newText}
            onChange={(e) => setNewText(e.target.value)}
            placeholder="Enter your text here..."
            className="min-h-[100px]"
          />
          <Button 
            onClick={handleSubmit}
            className="w-full"
          >
            Save Text
          </Button>
        </div>

        <div className="border rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">Previous Entries</h2>
          <ScrollArea className="h-[400px] w-full rounded-md border p-4">
            {entries?.map((entry) => (
              <div
                key={entry.id}
                className="mb-4 p-3 bg-secondary rounded-lg relative group"
              >
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => entry.id && handleDelete(entry.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
                <p className="whitespace-pre-wrap pr-8">{entry.content}</p>
                <p className="text-sm text-muted-foreground mt-2">
                  {new Date(entry.timestamp).toLocaleString()}
                </p>
              </div>
            ))}
            {!entries?.length && (
              <p className="text-muted-foreground text-center">
                No entries yet. Add your first one above!
              </p>
            )}
          </ScrollArea>
        </div>
      </div>
    </div>
  );
};

export default Index;